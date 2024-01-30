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
      self.df = yf.load_or_get_data(stock, self.period, self.interval)
      self.current_price = yf.find_current_price(self.df)
      self.scores[stock] = 1
      h += '<tr><td width=200>'
      h += html.stock_info(stock)
      h += '</td><td>'
      h += html.generate_price_chart(stock, self.df)
      h += '</td><td width=200>'
      h, self.scores[stock] = html.calculate_high_low(stock,
                                                      self.df,
                                                      self.current_price,
                                                      h,
                                                      self.avg_periods)
      h, self.scores[stock] = html.calculate_averages(stock,
                                                      self.df,
                                                      self.current_price,
                                                      h,
                                                      self.scores[stock],
                                                      self.avg_periods)
      self.color = yf.get_score_color(self.scores[stock])
      h += '<hr><table width=100%><tr><td bgcolor=' + self.color + '>'
      h += '<p><br><p><center>Score: ' + str(self.scores[stock])
      h += '<p><br><p></td></tr></table></td></tr>'

    h += '</table>'
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
