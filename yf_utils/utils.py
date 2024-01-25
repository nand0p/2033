import yfinance as yf
import pandas as pd
import warnings
import json

warnings.filterwarnings("ignore", category=FutureWarning) 


def download_quote(stock, period, interval):
  data = yf.download(stock, period=period, interval=interval)
  return data


def get_ticker(stock, period, interval):
  s = yf.Ticker(stock)
  hist = s.history(period=period, interval=interval)
  return hist[['Close']]


def save_csv(stock, df, path):
  df.to_csv(path + '/' + stock + '.csv')


def save_json(stock, df, path):
  j = df.to_json()
  with open(path + '/' + stock + '.json', 'w', encoding='utf-8') as f:
    json.dump(j, f, ensure_ascii=True, indent=4)


def save_images(stock, df, path):
  ax = df.plot.line()
  ax.figure.savefig(path + '/' + stock + '.png')


def find_low_price(df):
  low_price = round(float(str(df.min(axis=0)).split()[1]), 4)
  return low_price


def find_high_price(df):
  high_price = round(float(str(df.max(axis=0)).split()[1]), 4)
  return high_price


def find_current_price(df):
  current_price = round(float(str(df['Close'].iat[-1])), 4)
  return current_price


def find_average(df, dim):
  average = df['Close'].rolling(dim).mean()
  average = round(float(str(average).split()[-7]),4)
  return average


def current_compare(current, high):
  if current < high:
    color = 'green'
  else:
    color = 'red'
  return color
