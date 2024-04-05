from flask_classful import FlaskView, route, request
from utils import helpers, yf, disk, stocks
from flask import Flask, render_template, send_from_directory
import json
import os


app = Flask(__name__)


class X2033(FlaskView):
  def __init__(self):

    self.avg_periods = [ 9, 21, 50, 100, 200, 365, 420, 500, 1000 ]
    self.period = '10y'
    self.interval = '1d'
    self.tolerance = 0.075
    self.tolerance_averages = 0.01

    self.df = {}
    self.stocks = {}
    self.scores = {}
    self.results = {}
    self.category = 0
    self.speed = ''
    self.data_dir = './data/'
    self.s3_bucket = '2033.hex7.com'
    self.categories_file = 'categories.json'
    self.categories = stocks.get_categories(self.categories_file)
    self.debug = False


  @route('/', methods = ['GET'])
  def index(self):
    self.speed = request.args.get('speed', 'slow')
    self.category = request.args.get('cat', '0')

    if self.category == '9':
      self.stocks = {'AAPL': {'category': '9'}}
    else:
      self.stocks = stocks.get_stocks(os.environ.get('STOCKS'),
                                      self.category,
                                      self.categories)

    for stock in self.stocks:
      self.df[stock] = yf.load_or_get_data(stock=stock,
                                           period=self.period,
                                           interval=self.interval)
      self.stocks[stock]['score'] = 0
      self.stocks[stock]['averages'] = {}
      self.stocks[stock]['low'] = helpers.get_low_price(df=self.df[stock])
      self.stocks[stock]['high'] = helpers.get_high_price(df=self.df[stock])
      self.stocks[stock]['current_price'] = helpers.get_current_price(self.df[stock])
      self.stocks[stock]['current_color'] = helpers.get_current_color(
                                              current=self.stocks[stock]['current_price'],
                                              high=self.stocks[stock]['high'],
                                              tolerance=self.tolerance)

      self.stocks[stock]['info'] = helpers.stock_info(stock=stock)

      self.stocks[stock]['score'] = helpers.generate_price_chart(
                                      stock=stock,
                                      df=self.df[stock],
                                      tolerance=self.tolerance,
                                      debug=self.debug)

      self.stocks[stock]['score'] = helpers.calculate_high_low(
                                      current=self.stocks[stock]['current_price'],
                                      high=self.stocks[stock]['high'],
                                      avg_periods=self.avg_periods,
                                      tolerance=self.tolerance,
                                      score=self.stocks[stock]['score'] )

      (self.stocks[stock]['averages'], \
       self.stocks[stock]['score']) = helpers.calculate_averages(
                                        df=self.df[stock],
                                        score=self.stocks[stock]['score'],
                                        current=self.stocks[stock]['current_price'],
                                        tolerance=self.tolerance_averages,
                                        avg_periods=self.avg_periods,
                                        speed=self.speed)

      self.stocks[stock]['score_color'] = helpers.get_score_color(
                                            score=self.stocks[stock]['score'])


    self.scores = disk.save_scores(stocks=self.stocks,
                                   data_dir=self.data_dir,
                                   bucket=self.s3_bucket,
                                   speed=self.speed,
                                   debug=self.debug)


    return render_template('index.html',
                           debug=self.debug,
                           scores=self.scores,
                           stocks=self.stocks,
                           categories=self.categories,
                           cat_num=self.category,
                           speed=self.speed)


  @route('/test')
  def test(self):
    return 'success'


  @route('/stocks')
  def stocks(self):
    return self.stocks


  @route('/periods')
  def periods(self):
    return str(self.avg_periods)


  @route('/df')
  def df(self):
    return self.df


  @route('/results')
  def results(self):
    return self.results


  @route('/speed')
  def results(self):
    return self.speed


  @route('/robots.txt')
  def robots(self):
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'robots.txt', mimetype='text/plain')


  @route('/favicon.ico')
  def favicon(self):
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/x-icon')


X2033.register(app, route_base = '/')


if __name__ == "__main__":
  app.run(debug=True, passthrough_errors=True)
