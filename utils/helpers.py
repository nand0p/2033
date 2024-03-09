import yfinance as yf
import matplotlib
import textwrap
import math
import os


def get_current_price(df, precise=5):
  return round(df.Close.tail(1).values[0], precise)


def get_low_price(df, precise=5):
  return round(df.min(axis=0).values[0], precise)


def get_high_price(df, precise=5):
  return round(df.max(axis=0).values[0], precise)


def _find_average(df, dim, precise=5, debug=False):
  return round(df.Close.rolling(dim).mean().tail(1).values[0], precise)


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


def calculate_high_low(current, high, avg_periods, score, tolerance, precise=5):
  s = _current_compare(current, high, tolerance)
  if s == 2:
    return round(score + len(avg_periods) * 2.678, precise)
  elif s == 1:
    return round(score + len(avg_periods) / 2.456, precise)
  else:
    return round(score - len(avg_periods) - 2.901, precise)


def generate_price_chart(stock, df, tolerance, debug=False, precise=5):
  if not os.path.exists('/static/fast'):
    os.makedirs('/static/fast')
  if not os.path.exists('/static/slow'):
    os.makedirs('/static/slow')
  df['sma90'] = df.Close.rolling(window=90).mean()
  df['sma365'] = df.Close.rolling(window=365).mean()
  ax = df.plot.line()
  label = stock + ' prices'
  ax.set_title(label=label)
  ax.figure.savefig('/static/fast/' + stock + '.png')
  ax.figure.savefig('/static/slow/' + stock + '.png')
  matplotlib.pyplot.close()

  sma90 = df['sma90'].tail(1).values[0]
  sma365 = df['sma365'].tail(1).values[0]
  if debug:
    print('====>', stock, '<====')
    print('------>', 'sma90', sma90, '<------')
    print('------>', 'sma365', sma365, '<------')

  if math.isnan(sma90) or math.isnan(sma365):
    return 3
  else:
    ratio = sma90 / sma365
    if sma90 < sma365:
      if math.isclose(sma90, sma365, rel_tol=tolerance):
        return round(5.123 * ratio, precise)
      else:
        return round(10.456 * ratio, precise)
    else:
      return round(-5.789 * ratio, precise)


def calculate_averages(df, current, score, avg_periods, tolerance, speed):
  s = 0
  t = 0
  r = {}
  count = 1
  for period in sorted(avg_periods):
    r[period] = {}
    r[period]['price'] = _find_average(df, period)

    if math.isnan(r[period]['price']):
      s = -1
    else:
      s = _current_compare(current, r[period]['price'], tolerance)

    if speed == 'slow':
      # the longer the period (count), the greater the weight (t)
      if s == 2:
        t = count + 2.507
        color = 'green'
      elif s == 0:
        t = count * -2.109
        color = 'red'
      elif s == -1:
        t = count / 3 + 3.789
        color = 'blue'
      else:
        t = count / 1.5 + 2.012
        color = 'orange'
    elif speed == 'fast':
      # the shorter the period (count), the greater the weight (t)
      if s == 2:
        t = len(avg_periods) - count + 2.507
        color = 'green'
      elif s == 0:
        t = (len(avg_periods) - count) * -2.109
        color = 'red'
      elif s == -1:
        t = (len(avg_periods) - count) / 3 + 3.789
        color = 'blue'
      else:
        t = (len(avg_periods) - count) / 1.5 + 2.012
        color = 'orange'

    score = round(score + t, 4)
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


def get_current_color(current, high, tolerance):
  if current < high:
    if math.isclose(current, high, rel_tol=tolerance):
      return 'orange'
    else:
      return 'green'
  else:
    return 'red'
