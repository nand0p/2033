from flask_classful import FlaskView, route, request
from utils import helpers, yf, disk, stocks
from flask import Flask, render_template, send_from_directory
import json
import os


app = Flask(__name__)


class X2030(FlaskView):
  def __init__(self):
    self.df = {}
    self.stocks = {}
    self.avg_periods = [ 9, 21, 50, 100, 200, 365, 420, 500, 1000 ]
    self.period = '5y'
    self.interval = '1d'
    self.minimum_score = 25
    self.data_dir = './data/'
    self.tolerance = 0.075
    self.tolerance_averages = 0.01
    self.debug = False


  @route('/', methods = ['GET'])
  def index(self):
    cat = request.args.get('cat', '0')

    if cat == '7':
      self.stocks = {'AAPL': {'category': '7'}}
    else:
      self.stocks = stocks.get_stocks(os.environ.get('STOCKS'), cat)

    for stock in self.stocks:
      self.df[stock] = yf.load_or_get_data(stock, self.period, self.interval)
      self.stocks[stock]['score'] = 0
      self.stocks[stock]['averages'] = {}
      self.stocks[stock]['low'] = helpers.get_low_price(self.df[stock])
      self.stocks[stock]['high'] = helpers.get_high_price(self.df[stock])
      self.stocks[stock]['current_price'] = helpers.get_current_price(self.df[stock])
      self.stocks[stock]['current_color'] = helpers.get_current_color(
                                              current=self.stocks[stock]['current_price'],
                                              high=self.stocks[stock]['high'],
                                              tolerance=self.tolerance)

      self.stocks[stock]['info'] = helpers.stock_info(stock)

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
                                        avg_periods=self.avg_periods)

      self.stocks[stock]['score_color'] = helpers.get_score_color(
                                            self.stocks[stock]['score'])

    disk.save_scores(self.stocks, self.data_dir, debug=self.debug)
    return render_template('index.html', stocks=self.stocks, debug=self.debug)


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
