from flask import Flask, render_template, send_from_directory, jsonify
from flask_classful import FlaskView, route, request
from utils import scores, shares, stocks
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import json
import os


app = Flask(__name__)


class X2033(FlaskView):
  def __init__(self):
    self.total_money = 1000
    self.s_list = []
    self.savepath = 'static/'
    self.prefix = 'scores/'
    self.scores_key = 'scores_matrix.json'
    self.scores_file = 'scores_list.json'
    self.bucket = '2033.hex7.com'
    self.source_file = '2033.txt'
    self.api = 'http://' + self.bucket + '/'
    self.api_scores = self.api + self.prefix
    self.date = ''
    self.slow_dict = {}
    self.fast_dict = {}
    self.slow_results = {}
    self.slow_ordered = []
    self.fast_results = {}
    self.fast_ordered = []
    self.matrix = {}
    self.share_one = 0
    self.category = 0
    self.categories_file = 'categories.json'
    self.categories = stocks.get_categories(self.categories_file)
    self.debug = True

  @route('/', methods = ['GET'])
  def index(self):
    self.matrix = {}
    self.category = request.args.get('cat', '0')
    if int(self.category) < 0 or int(self.category) > 8:
      self.category = '0'
    self.debug = request.args.get('debug', False)
    self.total_money = int(request.args.get('cash', str(self.total_money)))
    self.date = datetime.now(ZoneInfo('US/Eastern')).isoformat().split('T')

    self.slow_dict = scores.get_url(self.api_scores + 'slow-' + self.date[0] + '.json',
                                    debug=self.debug)
    self.fast_dict = scores.get_url(self.api_scores + 'fast-' + self.date[0] + '.json',
                                    debug=self.debug)

    self.slow_results, \
    self.slow_ordered = scores.get_results(stocks=self.slow_dict,
                                           category=self.category,
                                           categories=self.categories,
                                           total_money=self.total_money,
                                           source_file=self.source_file,
                                           debug=self.debug)
    self.fast_results, \
    self.fast_ordered = scores.get_results(stocks=self.fast_dict,
                                           category=self.category,
                                           categories=self.categories,
                                           total_money=self.total_money,
                                           source_file=self.source_file,
                                           debug=self.debug)

    self.share_one = shares.get_min_shares(stocks=self.slow_dict,
                                           category=self.category,
                                           total_money=self.total_money,
                                           debug=self.debug)

    self.s_list = scores.get_scores_list(api=self.api,
                                         scores_file=self.scores_file,
                                         debug=self.debug)

    self.matrix = scores.get_matrix(s_list=self.s_list,
                                    slow_results=self.slow_results,
                                    fast_results=self.fast_results,
                                    source_file=self.source_file,
                                    bucket=self.bucket,
                                    category='0',
                                    debug=self.debug)

    scores.make_charts(matrix=self.matrix,
                       debug=self.debug,
                       savepath=self.savepath)

    scores.save_scores(matrix=self.matrix,
                       slow_results=self.slow_results,
                       fast_results=self.fast_results,
                       slow_ordered=self.slow_ordered,
                       fast_ordered=self.fast_ordered,
                       scores_key=self.scores_key,
                       savepath=self.savepath,
                       debug=self.debug)

    return render_template('index.html',
                           req=self.api,
                           req_scores=self.api_scores,
                           debug=self.debug,
                           s_list=self.s_list,
                           share_one=self.share_one,
                           datemade=' '.join(self.date),
                           slow_results=self.slow_results,
                           fast_results=self.fast_results,
                           slow_ordered=self.slow_ordered,
                           fast_ordered=self.fast_ordered,
                           categories=self.categories,
                           matrix=self.matrix)


  @route('/test')
  def test(self):
    return '200 success'


  @route('/slow_ordered')
  def json_slow_ordered(self):
    return send_from_directory(directory='static',
                               path='slow_ordered.json',
                               mimetype='application/json')


  @route('/fast_ordered')
  def json_fast_ordered(self):
    return send_from_directory(directory='static',
                               path='fast_ordered.json',
                               mimetype='application/json')


  @route('/slow_results')
  def json_slow_results(self):
    return send_from_directory(directory='static',
                               path='slow_results.json',
                               mimetype='application/json')


  @route('/fast_results')
  def json_fast_results(self):
    return send_from_directory(directory='static',
                               path='fast_results.json',
                               mimetype='application/json')


  @route('/matrix')
  def json_matrix(self):
    return send_from_directory(directory='static',
                               path='scores_matrix.json',
                               mimetype='application/json')


  @route('/robots.txt')
  def robots(self):
    return send_from_directory(directory='static',
                               path='robots.txt',
                               mimetype='text/plain')


  @route('/favicon.ico')
  def favicon(self):
    return send_from_directory(directory='static',
                               path='favicon.ico',
                               mimetype='image/x-icon')


X2033.register(app, route_base = '/')


if __name__ == "__main__":
  app.run(debug=True, passthrough_errors=True)
