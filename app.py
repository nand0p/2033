from flask_classful import FlaskView, route
from utils import html, yf, disk
from flask import Flask
import os


app = Flask(__name__)


class X2030(FlaskView):
  def __init__(self):
    self.stocks = sorted(os.environ.get('STOCKS').strip('\"').upper().split())
    self.avg_periods = [ 9, 21, 50, 75, 100, 200, 365, 500 ]
    self.period = '5y'
    self.interval = '1d'
    self.minimum_score = 25
    self.data_dir='./data/'
    self.scores = {}
    self.df = None
    self.current_price = None
    self.color = None


  def index(self):
    h = html.header(self.stocks)
    for stock in self.stocks:
      self.scores[stock] = 1
      self.df = yf.load_or_get_data(stock, self.period, self.interval)
      self.current_price = yf.find_current_price(self.df)
      h += html.stock_info(stock)
      h, self.scores[stock] = html.generate_price_chart(stock=stock,
                                                        df=self.df,
                                                        html=h,
                                                        score=self.scores[stock])
      h, self.scores[stock] = html.calculate_high_low(stock=stock,
                                                      df=self.df,
                                                      price=self.current_price,
                                                      html=h,
                                                      score=self.scores[stock],
                                                      avg_periods=self.avg_periods)
      h, self.scores[stock] = html.calculate_averages(stock=stock,
                                                      df=self.df,
                                                      price=self.current_price,
                                                      html=h,
                                                      score=self.scores[stock],
                                                      avg_periods=self.avg_periods)
      self.color = yf.get_score_color(self.scores[stock])
      h += html.scores(self.color, self.scores[stock])

    h += html.footer(self.scores, self.minimum_score)
    disk.save_scores(self.scores, self.data_dir)
    return h


  @route('/test')
  def test(self):
    return 'success'


  @route('/stocks')
  def stocks(self):
    return str(self.stocks)


  @route('/periods')
  def periods(self):
    return str(self.avg_periods)


X2030.register(app, route_base = '/')

if __name__ == "__main__":
  app.run(debug=True, passthrough_errors=True)
