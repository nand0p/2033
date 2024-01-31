from flask_classful import FlaskView, route
from utils import html, yf, disk
from flask import Flask
import json
import os


app = Flask(__name__)


class X2030(FlaskView):
  def __init__(self):
    self.stocks = disk.get_stocks(os.environ.get('STOCKS'))
    self.avg_periods = [ 9, 21, 50, 75, 100, 200, 365, 500 ]
    self.period = '5y'
    self.interval = '1d'
    self.minimum_score = 25
    self.data_dir = './data/'
    self.scores = {}
    self.df = {}
    self.current_price = {}
    self.color = {}
    self.html = ''


  def index(self):
    self.html = html.header(self.stocks)

    for stock in self.stocks:
      self.scores[stock] = 1
      self.df[stock] = yf.load_or_get_data(stock, self.period, self.interval)
      self.current_price[stock] = yf.get_current_price(self.df[stock])

      self.html += html.stock_info(stock)
      self.html, self.scores[stock] = html.generate_price_chart(stock=stock,
                                                        df=self.df[stock],
                                                        html=self.html,
                                                        score=self.scores[stock])
      self.html, self.scores[stock] = html.calculate_high_low(stock=stock,
                                                      df=self.df[stock],
                                                      html=self.html,
                                                      price=self.current_price[stock],
                                                      score=self.scores[stock],
                                                      avg_periods=self.avg_periods)
      self.html, self.scores[stock] = html.calculate_averages(stock=stock,
                                                      df=self.df[stock],
                                                      html=self.html,
                                                      price=self.current_price[stock],
                                                      score=self.scores[stock],
                                                      avg_periods=self.avg_periods)
      self.color[stock] = yf.get_score_color(self.scores[stock])
      self.html += html.scores(self.color[stock], self.scores[stock])

    self.html += html.footer(self.stocks, self.scores, self.minimum_score)
    disk.save_scores(self.scores, self.data_dir)
    return self.html


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
