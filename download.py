from utils import yf, disk
import os


img_path = 'images/stocks/'
data_path = 'data/stocks/'
text_file = open("2033.txt", "r")
lines = text_file.readlines()
text_file.close()


if not os.path.exists(img_path):
  os.makedir(img_path)

if not os.path.exists(data_path):
  os.makedir(data_path)


for stock in lines:
  stock = stock.upper().strip()
  df = yf.get_ticker(stock, period='max', interval='1d')
  disk.save_images(stock, df, img_path)
  disk.save_csv(stock, df, data_path)
  disk.save_json(stock, df, data_path)
