from yf_utils import utils
from flask import Flask

import yfinance as yf
import matplotlib
import textwrap
import os


app = Flask(__name__)
stocks = []
app.config['STOCKS'] = os.environ.get('STOCKS')
stocks = sorted(app.config['STOCKS'].strip('\"').upper().split())
avg_periods = [ 9, 21, 50, 75, 100, 200, 365, 500 ]
period = '5y'
interval = '1d'
minimum_score = 25

 
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

  # high-low is double score value
  if s > 0:
    s = s * len(avg_periods)
  else:
    s = s * -(len(avg_periods))

  score = score + s
  html += '<p>LOW: ' + str(low)
  html += '<p>HIGH: ' + str(high)
  html += '<p style="color:' + color + ';">CURRENT: ' + str(current) + '</p>'
  return html, score


def calculate_averages(stock, df, current, html, score):
  html += '<hr>'
  count = 1
  for period in avg_periods:
    average = utils.find_average(df, period)
    color, s = utils.current_compare(current, average)

    # the longer the period, the more the weight
    if s > 0:
      s = s + count
    if s == 0:
      s = s - count
    score = score + s

    html += '<p style="color:' + color + \
            ';">AVG ' + str(period) + ': ' + \
            str(average) + '</p>'
    count = count + 1
  return html, score


def stock_info(stock):
  html = ''
  s = yf.Ticker(stock)
  try:
    stock_info = s.info
  except:
    stock_info = {'longBusinessSummary':'None'}
  html += '<h2><center>' + stock + '</center></h2>'
  html += '<p>' + textwrap.shorten(str(stock_info.get('longBusinessSummary')),
                                   width=100,
                                   placeholder="...")
  return html


def footer(score, minimum_score):
  html = '</table><p><br><p><hr><center><b>'
  score = sorted(score.items(), key=lambda x: x[1], reverse=True)
  for stock, score in score:
    if score >= minimum_score:
      html += '<h1><font color=green>' + stock + ': ' + str(score) + '</font></h1>'
    elif score >= 0:
      html += '<h3>' + stock + ': ' + str(score) + '</h3>'
    else:
      html += '<h6>' + stock + ': ' + str(score) + '</h6>'
  html += '<p><br><p><center><a href=https://github.com/nand0p/2030>'
  html += 'https://github.com/nand0p/2030</a><body></html>'
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
    score[stock] = 1
    df = utils.load_or_get_data(stock, period, interval)
    current = utils.find_current_price(df)
    html += '<tr><td width=200>'
    html += stock_info(stock)
    html += '</td><td>'
    html += generate_price_chart(stock, df)
    html += '</td><td width=200>'
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
