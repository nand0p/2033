import yfinance as yf
import pandas as pd
import matplotlib
import warnings
import json

warnings.filterwarnings("ignore", category=FutureWarning) 


def get_score_color(score):
  if score > 10:
    return 'green'
  elif score > 5:
    return 'yellow'
  else:
    return 'red'

def load_or_get_data(stock, period, interval):
  df = get_ticker(stock, period=period, interval=interval)
  return df


def download_quote(stock, period, interval):
  data = yf.download(stock, period=period, interval=interval)
  return data


def get_ticker(stock, period, interval):
  s = yf.Ticker(stock)
  hist = s.history(period=period, interval=interval)
  return hist[['Close']]


def find_current_price(df):
  current_price = round(float(str(df.get('Close').iat[-1])), 4)
  return current_price
