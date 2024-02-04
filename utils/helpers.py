import yfinance as yf
import matplotlib
import textwrap
import math
import os


def get_low_price(df):
  low_price = round(float(str(df.min(axis=0)).split()[1]), 4)
  return low_price


def get_high_price(df):
  high_price = round(float(str(df.max(axis=0)).split()[1]), 4)
  return high_price


def _find_average(df, dim):
  average = df['Close'].rolling(dim).mean()
  average = round(float(str(average).split()[-7]),4)
  return average


def _current_compare(current, test):
  if current/test <= 0.94:
    return 2
  elif current/test >= 0.99:
    return 0
  else:
    return 1


def calculate_high_low(current, high, avg_periods, score):
  s = _current_compare(current, high)
  if s > 0:
    s = s * len(avg_periods)
  else:
    s = s * -(len(avg_periods))

  score = score + s
  return score


def generate_price_chart(stock, df):
  ax = df.plot.line()
  df['sma90'] = df.Close.rolling(window=90).mean()
  df['sma365'] = df.Close.rolling(window=365).mean()
  ax = df.plot.line()
  ax.figure.savefig('static/' + stock + '.png')
  matplotlib.pyplot.close()

  if int(df['sma90'][-1]) < int(df['sma365'][-1]):
    return 20
  else:
    return -10


def calculate_averages(df, current, score, avg_periods):
  r = {}
  count = 1
  for period in sorted(avg_periods):
    r[period] = {}
    r[period]['price'] = _find_average(df, period)
    s = _current_compare(current, r[period]['price'])

    # the longer the period, the greater the weight
    if s == 2:
      s = s + count
      color = 'green'
    elif s == 0:
      s = s - count
      color = 'red'
    else:
      color = 'orange'

    score = score + s
    count = count + 1
    r[period]['color'] = color

  return r, score


def stock_info(stock):
  s = yf.Ticker(stock)
  try:
    stock_info = s.info
  except:
    stock_info = {'longBusinessSummary':'None'}

  return textwrap.shorten(str(stock_info.get('longBusinessSummary')),
                          width=250, placeholder="...")


def get_score_color(score):
  if score > 10:
    return 'green'
  elif score > 5:
    return 'yellow'
  else:
    return 'red'


def get_current_price(df):
  current_price = round(float(str(df.get('Close').iat[-1])), 4)
  return current_price


def get_current_color(current, high, tolerance):
  if current < high:
    if math.isclose(current, high, rel_tol=tolerance):
      return 'orange'
    else:
      return 'green'
  else:
    return 'red'
