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
  r = {}

  for stock in stocks:
    s, v = stock.split(':')
    if v == cat or cat == '0':
      r[s] = {}
      r[s]['ticker'] = s
      r[s]['category'] = v

  return r


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
