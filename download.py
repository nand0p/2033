from yf_utils import utils
import pandas as pd
import yfinance as yf
import os


img_path = 'images'
data_path = 'data'
text_file = open("2030.txt", "r")
lines = text_file.readlines()
text_file.close()


if not os.path.exists(img_path):
  os.makedir(img_path)

if not os.path.exists(data_path):
  os.makedir(data_path)


for stock in lines:
  stock = stock.upper().strip()
  df = utils.get_ticker(stock, period='max', interval='1d')
  utils.save_images(stock, df, 'images/')
  utils.save_csv(stock, df, 'data/')
  utils.save_json(stock, df, 'data/')
