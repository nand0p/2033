from flask import Flask
from yf_utils import utils
import yfinance as yf
import matplotlib
import os


app = Flask(__name__)
stocks = []
app.config['STOCKS'] = os.environ.get('STOCKS')
stocks = app.config['STOCKS'].strip('\"').upper().split()

 
def load_or_get_data(stock):
  df = utils.get_ticker(stock, period='5y', interval='1d')
  return df


def generate_price_chart(stock, df):
  html = ''
  ax = df.plot.line()
  ax.figure.savefig('static/' + stock + '.png')
  html += '<center><img src=static/' + stock + '.png></center>'
  return html


def calculate_high_low(stock, df):
  html = ''
  low = utils.find_low_price(df)
  high = utils.find_high_price(df)
  current = utils.find_current_price(df)
  color = utils.current_compare(current, high)
  html += '<p>LOW: ' + str(low)
  html += '<p>HIGH: ' + str(high)
  html += '<p style="color:' + color + ';">CURRENT: ' + str(current) + '</p>'
  return html


def calculate_averages(stock, df):
  html = '<hr>'
  current = utils.find_current_price(df)
  short_avg = utils.find_average(df, 15)
  medium_avg = utils.find_average(df, 60)
  long_avg = utils.find_average(df, 200)
  color = utils.current_compare(current, short_avg)
  html += '<p style="color:' + color + ';">ShortAVG: ' + str(short_avg) + '</p>'
  color = utils.current_compare(current, medium_avg)
  html += '<p style="color:' + color + ';">MediumAVG: ' + str(medium_avg) + '</p>'
  color = utils.current_compare(current, long_avg)
  html += '<p style="color:' + color + ';">LongAVG: ' + str(long_avg) + '</p>'
  return html


def stock_info(stock):
  html = ''
  s = yf.Ticker(stock)
  stock_info = s.info
  html += '<h2><center>' + stock + '</center></h2>'
  html += '<p>' + str(stock_info['longBusinessSummary'])
  return html


@app.route('/')
def flaskapp():
  html = ''
  html += '<html><head><title>Stock Hunter</title></head><body>'
  html += '<h1>Stock Hunter</h1>'
  html += str(stocks)
  html += '<table border=3 colspan=3 width=100%>'
      
  for stock in stocks:
    df = load_or_get_data(stock)
    html += '<tr><td>'
    html += stock_info(stock)
    html += '</td><td>'
    html += generate_price_chart(stock, df)
    html += '</td><td width=150>'
    html += calculate_high_low(stock, df)
    html += calculate_averages(stock, df)
    html += '</td></tr>'

  html += '</table><body></html>'

  return html


@app.route('/test')
def test():
  return 'success'


if __name__ == "__main__":
  app.run(debug=True)
