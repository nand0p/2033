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
    self.html = html.header(self.stocks)
    self.scores = {}
    self.df = None
    self.current_price = None
    self.color = None


  def index(self):
    for stock in self.stocks:
      self.df = yf.load_or_get_data(stock, self.period, self.interval)
      self.current_price = yf.find_current_price(self.df)
      self.scores[stock] = 1
      self.html += '<tr><td width=200>'
      self.html += html.stock_info(stock)
      self.html += '</td><td>'
      self.html += html.generate_price_chart(stock, self.df)
      self.html += '</td><td width=200>'
      self.html, self.scores[stock] = html.calculate_high_low(stock,
                                                              self.df,
                                                              self.current_price,
                                                              self.html,
                                                              self.scores[stock],
                                                              self.avg_periods)
      self.html, self.scores[stock] = html.calculate_averages(stock,
                                                              self.df,
                                                              self.current_price,
                                                              self.html,
                                                              self.scores[stock],
                                                              self.avg_periods)
      self.color = yf.get_score_color(self.scores[stock])
      self.html += '<hr><table width=100%><tr><td bgcolor=' + self.color + '>'
      self.html += '<p><br><p><center>Score: ' + str(self.scores[stock])
      self.html+= '<p><br><p></td></tr></table></td></tr>'

    self.html += html.footer(self.scores, self.minimum_score)
    disk.save_scores(self.scores, self.data_dir)
    return self.html

  @route('/test')
  def test(self):
    return 'success'


X2030.register(app, route_base = '/')

if __name__ == "__main__":
  app.run(debug=True, passthrough_errors=True)
