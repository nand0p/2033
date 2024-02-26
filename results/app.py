from flask import Flask, render_template, send_from_directory
from flask_classful import FlaskView, route, request
from utils import scores
import datetime
import requests
import json
import os


app = Flask(__name__)


class X2030(FlaskView):
  def __init__(self):
    self.total_money = 1000
    self.results = {}
    self.ordered = []
    self.api = 'http://2030.hex7.com/scores/'
    self.date = ''
    self.debug = False

  @route('/', methods = ['GET'])
  def index(self):
    category = request.args.get('cat', '0')
    self.total_money = int(request.args.get('cash', str(self.total_money)))
    self.date = datetime.datetime.now().isoformat().split('T')[0]
    req = self.api + 'scores-' + self.date + '.json'
    r = requests.get(req)
    r_dict = json.loads(r.text)

    if self.debug:
      print('<p>api:<br>',
            self.api,
            '<p>date:<br>',
            self.date,
            '<p>stocks:<br>',
            str(r.content),
            '<p>response:<br>',
            str(r_dict),
            '<p><br>p>')

    self.results, \
    self.ordered = scores.get_results(stocks=json.loads(r.text),
                                      category=category,
                                      total_money=self.total_money,
                                      debug=self.debug)

    return render_template('index.html',
                           debug=self.debug,
                           datemade=self.date,
                           ordered=self.ordered,
                           results=self.results)


  @route('/test')
  def test(self):
    return 'success'


  @route('/api')
  def results(self):
    return self.api


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
