import yfinance as yf
import matplotlib
import textwrap
import math
import os


def get_low_price(df):
  low_price = round(df.min(axis=0).values[0], 4)
  return low_price


def get_high_price(df):
  return round(df.max(axis=0).values[0], 4)


def _find_average(df, dim):
  if len(df.index) < dim:
    dim = len(df.index)

  return round(df['Close'].rolling(dim).mean().tail(1).values[0], 4)


def _current_compare(current, test, tolerance):
  low = 0.94
  high = 0.99
  ratio = current / test
  if ratio <= low:
    if math.isclose(ratio, low, rel_tol=tolerance):
      return 1
    else:
      return 2
  elif ratio >= high:
    if math.isclose(ratio, high, rel_tol=tolerance):
      return 1
    else:
      return 0
  else:
    return 1


def calculate_high_low(current, high, avg_periods, score, tolerance):
  s = _current_compare(current, high, tolerance)
  if s == 2:
    s = s * len(avg_periods)
  elif s == 1:
    s = s * int(len(avg_periods) / 2)
  else:
    s = -(len(avg_periods))

  score = score + s
  return score


def generate_price_chart(stock, df, tolerance, debug=False):
  df['sma90'] = df.Close.rolling(window=90).mean()
  df['sma365'] = df.Close.rolling(window=365).mean()
  ax = df.plot.line()
  ax.figure.savefig('static/' + stock + '.png')
  matplotlib.pyplot.close()

  if debug:
    print('====>', stock, '<====')
    print('------>', df['sma90'], '<------')
    print('------>', df['sma365'], '<------')

  if df['sma90'][-1] < df['sma365'][-1]:
    if math.isclose(df['sma90'][-1], df['sma365'][-1], rel_tol=tolerance):
      return 5
    else:
      return 20
  else:
    return -10


def calculate_averages(df, current, score, avg_periods, tolerance):
  r = {}
  count = 1
  for period in sorted(avg_periods):
    r[period] = {}
    r[period]['price'] = _find_average(df, period)
    s = _current_compare(current, r[period]['price'], tolerance)

    # the longer the period, the greater the weight
    if s == 2:
      s = s + count
      color = 'green'
    elif s == 0:
      s = s - count - 2
      color = 'red'
    else:
      s = s - int(count/2) - 1
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
                          width=600, placeholder="...")


def get_score_color(score):
  if score > 33:
    return 'green'
  elif abs(score) <= 33:
    return 'yellow'
  else:
    return 'red'


def get_current_price(df):
  current_price = round(df['Close'].tail(1).values[0], 4)
  return current_price


def get_current_color(current, high, tolerance):
  if current < high:
    if math.isclose(current, high, rel_tol=tolerance):
      return 'orange'
    else:
      return 'green'
  else:
    return 'red'
