from flask_classful import FlaskView, route, request
from utils import helpers, yf, disk
from flask import Flask, render_template
import json
import os


app = Flask(__name__)


class X2030(FlaskView):
  def __init__(self):
    self.df = {}
    self.stocks = {}
    self.avg_periods = [ 9, 21, 50, 75, 100, 200, 365, 500 ]
    self.period = '5y'
    self.interval = '1d'
    self.minimum_score = 25
    self.data_dir = './data/'
    self.tolerance = 0.075


  @route('/', methods = ['GET'])
  def index(self):
    self.stocks = disk.get_stocks(os.environ.get('STOCKS'),
                                  request.args.get('cat', '0'))

    for stock in self.stocks:
      self.df[stock] = yf.load_or_get_data(stock, self.period, self.interval)
      self.stocks[stock]['score'] = 0
      self.stocks[stock]['averages'] = {}
      self.stocks[stock]['low'] = helpers.get_low_price(self.df[stock])
      self.stocks[stock]['high'] = helpers.get_high_price(self.df[stock])
      self.stocks[stock]['current_price'] = helpers.get_current_price(self.df[stock])
      self.stocks[stock]['current_color'] = helpers.get_current_color(
                                              self.stocks[stock]['current_price'],
                                              self.stocks[stock]['high'],
                                              self.tolerance)

      self.stocks[stock]['info'] = helpers.stock_info(stock)

      self.stocks[stock]['score'] = helpers.generate_price_chart(
                                      stock=stock,
                                      df=self.df[stock])

      self.stocks[stock]['score'] = helpers.calculate_high_low(
                                      current=self.stocks[stock]['current_price'],
                                      high=self.stocks[stock]['high'],
                                      avg_periods=self.avg_periods,
                                      score=self.stocks[stock]['score'] )

      (self.stocks[stock]['averages'], \
       self.stocks[stock]['score']) = helpers.calculate_averages(
                                        df=self.df[stock],
                                        score=self.stocks[stock]['score'],
                                        current=self.stocks[stock]['current_price'],
                                        avg_periods=self.avg_periods)

      self.stocks[stock]['score_color'] = helpers.get_score_color(
                                            self.stocks[stock]['score'])

    #disk.save_scores(self.scores, self.data_dir)
    return render_template('index.html', stocks=self.stocks)


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


X2030.register(app, route_base = '/')

if __name__ == "__main__":
  app.run(debug=True, passthrough_errors=True)
