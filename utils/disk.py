import matplotlib
import datetime
import boto3    
import json

s3 = boto3.resource('s3')
bucket = '2030.hex7.com'
date = datetime.datetime.now().isoformat().split('T')[0]
scores_key = 'scores-' + date + '.json'


def get_stocks(stocks, cat):
  stocks = sorted(set(stocks.strip('\"').upper().split()))
  stocks_1 = []  #  large cap
  stocks_2 = []  #  small cap
  stocks_3 = []  #  cloud etf
  stocks_4 = []  #  biotech
  stocks_5 = []  #  renewable

  for stock in stocks:
    s, v = stock.split(':')
    if int(v) == 1:
      stocks_1.append(s)
    elif int(v) == 2:
      stocks_2.append(s)
    elif int(v) == 3:
      stocks_3.append(s)
    elif int(v) == 4:
      stocks_4.append(s)
    elif int(v) == 5:
      stocks_5.append(s)

  if int(cat) == 1:
    return stocks_1
  elif int(cat) == 2:
    return stocks_2
  elif int(cat) == 3:
    return stocks_3
  elif int(cat) == 4:
    return stocks_4
  elif int(cat) == 5:
    return stocks_5
  else:
    return stocks_1 + stocks_2 + stocks_3 + stocks_4 + stocks_5


def save_scores(scores, data_dir):
  with open(data_dir + scores_key, 'w') as out:
    json.dump(scores, out, ensure_ascii=True, indent=4)

  #s3object = s3.Object(bucket, scores_key)
  #s3object.put( Body=(bytes(json.dumps(scores).encode('UTF-8'))))


def save_csv(stock, df, path):
  df.to_csv(path + '/' + date + '-' + stock + '.csv')


def save_json(stock, df, path):
  j = df.to_json()
  with open(path + '/' + date + '-' + stock + '.json', 'w', encoding='utf-8') as f:
    json.dump(j, f, ensure_ascii=True, indent=4)


def save_images(stock, df, path):
  ax = df.plot.line()
  ax.figure.savefig(path + '/' + date + '-' +  stock + '.png')
  matplotlib.pyplot.close()
