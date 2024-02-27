from flask import Flask, render_template, send_from_directory
from flask_classful import FlaskView, route, request
from utils import scores, shares
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import json
import os


app = Flask(__name__)


class X2030(FlaskView):
  def __init__(self):
    self.total_money = 1000
    self.results = {}
    self.ordered = []
    self.s_list = []
    self.savepath = 'static/'
    self.prefix = 'scores/'
    self.bucket = '2030.hex7.com'
    self.api = 'http://' + self.bucket + '/' + self.prefix
    self.date = ''
    self.req = ''
    self.r_dict = {}
    self.matrix = {}
    self.share_one = 0
    self.category = 0
    self.debug = False

  @route('/', methods = ['GET'])
  def index(self):
    self.matrix = {}
    self.category = request.args.get('cat', '0')
    self.debug = request.args.get('debug', False)
    self.total_money = int(request.args.get('cash', str(self.total_money)))
    self.date = datetime.now(ZoneInfo('US/Eastern')).isoformat().split('T')
    self.req = self.api + 'scores-' + self.date[0] + '.json'
    r = requests.get(self.req)
    if r.status_code != 200:
      raise Exception("req: ", self.req, " status code: ", r.status_code)

    self.r_dict = json.loads(r.text)

    if self.debug:
      print('<p>req:<br>', self.req,
            '<p>api:<br>', self.api,
            '<p>date:<br>', self.date,
            '<p>stocks:<br>', str(r.content),
            '<p>response:<br>', str(self.r_dict),
            '<p><br>p>')

    self.results, \
    self.ordered = scores.get_results(stocks=self.r_dict,
                                      category=self.category,
                                      total_money=self.total_money,
                                      debug=self.debug)

    self.share_one = shares.get_min_shares(stocks=self.r_dict,
                                           category=self.category,
                                           total_money=self.total_money,
                                           debug=self.debug)

    self.s_list = scores.get_scores_list(bucket=self.bucket,
                                         prefix=self.prefix,
                                         debug=self.debug)

    for key in self.s_list:
      req = 'http://' + self.bucket + '/' + key

      r = requests.get(req)
      r_dict = json.loads(r.text)
      if self.debug:
        print('key', key)
        print('req', req)
        print('r_dict', r_dict)

      for k, v in r_dict.items():
        if self.results[k]['category'] == self.category or \
           self.category == '0' and \
           self.results[k]['category'] != '6':

          if k not in self.matrix:
            self.matrix[k] = []
          self.matrix[k].append(round(v['score'], 2))

    scores.make_charts(matrix=self.matrix,
                       debug=self.debug,
                       savepath=self.savepath)

    return render_template('index.html',
                           req=self.req,
                           debug=self.debug,
                           datemade=' '.join(self.date),
                           share_one=self.share_one,
                           ordered=self.ordered,
                           results=self.results,
                           matrix=self.matrix)


  @route('/test')
  def test(self):
    return '200 success'


  @route('/robots.txt')
  def robots(self):
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')


  @route('/favicon.ico')
  def favicon(self):
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/x-icon')


X2030.register(app, route_base = '/')


if __name__ == "__main__":
  app.run(debug=True, passthrough_errors=True)
