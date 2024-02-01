import yfinance as yf
import matplotlib
import textwrap
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
    return (2, 'red')
  elif current/test >= 0.99:
    return (0, 'yellow')
  else:
    return (1, 'green')


def calculate_high_low(current, high, avg_periods):
  (score, color) = _current_compare(current, high)
  if score > 0:
    return score * len(avg_periods) + score
  else:
    return score -(len(avg_periods)) 


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



def calculate_averages(df, high, score, avg_periods):
  r = {}
  count = 1
  for period in sorted(avg_periods):
    r[period] = {}
    r[period]['price'] = _find_average(df, period)
    (s, r[period]['color']) = _current_compare(high, r[period]['price'])

    # the longer the period, the more the weight
    if s > 0:
      s = s + count
    if s == 0:
      s = s - count

    score = score + s
    count = count + 1

  return r, score


def stock_info(stock):
  s = yf.Ticker(stock)
  try:
    stock_info = s.info
  except:
    stock_info = {'longBusinessSummary':'None'}

  return textwrap.shorten(str(stock_info.get('longBusinessSummary')),
                          width=250, placeholder="...")
