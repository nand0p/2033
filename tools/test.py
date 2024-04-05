from yf_utils import utils
import pandas as pd
import yfinance as yf
import os


img_path = 'images'
data_path = 'data'
text_file = open("2033.txt", "r")
lines = text_file.readlines()
text_file.close()


stock = lines[0]
stock = stock.upper().strip()
s = yf.Ticker(stock)
print(s.earnings_dates)
