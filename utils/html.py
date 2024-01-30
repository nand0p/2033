import yfinance as yf
import matplotlib
import textwrap
import os


def _find_low_price(df):
  low_price = round(float(str(df.min(axis=0)).split()[1]), 4)
  return low_price


def _find_high_price(df):
  high_price = round(float(str(df.max(axis=0)).split()[1]), 4)
  return high_price


def _find_average(df, dim):
  average = df['Close'].rolling(dim).mean()
  average = round(float(str(average).split()[-7]),4)
  return average


def _current_compare(current, test):
  if current/test <= 0.94:
    color = 'green'
    score = 2
  elif current/test >= 0.99:
    color = 'red'
    score = 0
  else:
    color = 'yellow'
    score = 1
  return color, score


def calculate_high_low(stock, df, current, html, avg_periods):
  score = 0
  low = _find_low_price(df)
  high = _find_high_price(df)
  color, s = _current_compare(current, high)

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


def header(stocks):
  html = ''
  html += '<html><head><!-- Google tag (gtag.js) -->'
  html += '<script async src="https://www.googletagmanager.com/gtag/js?id=G-3SZL2VYX8Q">'
  html += '</script><script>window.dataLayer = window.dataLayer || [];'
  html += 'function gtag(){dataLayer.push(arguments);}'
  html += 'gtag("js", new Date()); gtag("config", "G-3SZL2VYX8Q");</script>'
  html += '<title>Stock Hunter</title></head><body>'
  html += '<h1>Stock Hunter</h1>'
  html += str(stocks)
  html += '<table border=3 colspan=3 width=100%>'
  return html



def generate_price_chart(stock, df):
  html = ''
  ax = df.plot.line()
  ax.figure.savefig('static/' + stock + '.png')
  matplotlib.pyplot.close()
  html += '<center><img src=static/' + stock + '.png></center>'
  return html



def calculate_averages(stock, df, current, html, score, avg_periods):
  html += '<hr>'
  count = 1
  for period in avg_periods:
    average = _find_average(df, period)
    color, s = _current_compare(current, average)

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
  html = '<p><br><p><hr><center><b>'
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
