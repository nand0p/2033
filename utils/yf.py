import yfinance as yf
import pandas as pd
import matplotlib
import warnings
import json

warnings.filterwarnings("ignore", category=FutureWarning) 


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
