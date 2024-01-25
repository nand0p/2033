from yf_utils import utils
from flask import Flask

import yfinance as yf
import matplotlib
import os


app = Flask(__name__)
stocks = []
app.config['STOCKS'] = os.environ.get('STOCKS')
stocks = app.config['STOCKS'].strip('\"').upper().split()
avg_periods = [ 5, 10, 20, 50, 100, 200, 500 ]
period = '5y'
interval = '1d'
minimum_score = 10

 
def generate_price_chart(stock, df):
  html = ''
  ax = df.plot.line()
  ax.figure.savefig('static/' + stock + '.png')
  matplotlib.pyplot.close()
  html += '<center><img src=static/' + stock + '.png></center>'
  return html


def calculate_high_low(stock, df, current, html, score):
  low = utils.find_low_price(df)
  high = utils.find_high_price(df)
  color, s = utils.current_compare(current, high)
  score = score + s
  html += '<p>LOW: ' + str(low)
  html += '<p>HIGH: ' + str(high)
  html += '<p style="color:' + color + ';">CURRENT: ' + str(current) + '</p>'
  return html, score


def calculate_averages(stock, df, current, html, score):
  html += '<hr>'
  for period in avg_periods:
    average = utils.find_average(df, period)
    color, s = utils.current_compare(current, average)
    score = score + s
    html += '<p style="color:' + color + \
            ';">AVG ' + str(period) + ': ' + \
            str(average) + '</p>'
  return html, score


def stock_info(stock):
  html = ''
  s = yf.Ticker(stock)
  stock_info = s.info
  html += '<h2><center>' + stock + '</center></h2>'
  html += '<p>' + str(stock_info['longBusinessSummary'])
  return html


def footer(score, minimum_score):
  html = '</table><p><br><p><hr><center><b>'
  score = sorted(score.items(), key=lambda x: x[1], reverse=True)
  for stock, score in score:
    if score >= minimum_score:
      html += stock + ': ' + str(score) + '<br>'
  html += '<body></html>'
  return html



@app.route('/')
def flaskapp():
  html = ''
  html += '<html><head><title>Stock Hunter</title></head><body>'
  html += '<h1>Stock Hunter</h1>'
  html += str(stocks)
  html += '<table border=3 colspan=3 width=100%>'
      
  score = {}
  for stock in stocks:
    score[stock] = 0
    df = utils.load_or_get_data(stock, period, interval)
    current = utils.find_current_price(df)
    html += '<tr><td>'
    html += stock_info(stock)
    html += '</td><td>'
    html += generate_price_chart(stock, df)
    html += '</td><td width=150>'
    html, score[stock] = calculate_high_low(stock, df, current, html, score[stock])
    html, score[stock] = calculate_averages(stock, df, current, html, score[stock])
    color = utils.get_score_color(score[stock])
    html += '<hr><table width=100%><tr><td bgcolor=' + color + '>'
    html += '<p><br><p><center>Score: ' + str(score[stock])
    html += '<p><br><p></td></tr></table></td></tr>'

  html += footer(score, minimum_score)

  return html


@app.route('/test')
def test():
  return 'success'


if __name__ == "__main__":
  app.run(debug=True, passthrough_errors=True)
