from datetime import datetime
import matplotlib
import operator
import boto3    
import json
import os


def save_scores(stocks, speed, bucket, data_dir, save_to_s3=False, debug=False):
  scores_out = {}
  date = datetime.now().isoformat().split('T')[0]
  scores_key = speed + '-' + date + '.json'

  if not os.path.exists(data_dir):
    os.makedirs(data_dir)

  for stock in stocks.keys():
    if stocks[stock]['score'] > 100:
      stocks[stock]['score'] = 99.999
    elif stocks[stock]['score'] < -100:
      stocks[stock]['score'] = -99.999
    stocks[stock]['score'] = round(stocks[stock]['score'], 3)

    scores_out[stock] = {}
    scores_out[stock]['score'] = stocks[stock]['score']
    scores_out[stock]['current_price'] = stocks[stock]['current_price']
    scores_out[stock]['category'] = stocks[stock]['category']

    if debug:
      print('stock', stock)
      print('score', scores_out[stock]['score'])
      print('current_price', scores_out[stock]['current_price'])

  with open(data_dir + scores_key, 'w') as out:
    json.dump(scores_out, out, ensure_ascii=True, indent=4)

  if save_to_s3:
    s3 = boto3.resource('s3')
    s3object = s3.Object(bucket, scores_key)
    s3object.put(Body=(bytes(json.dumps(scores).encode('UTF-8'))))

  scores_sort = {}
  for stock in stocks.keys():
    scores_sort.update({stocks[stock]['score']: stock})

  if debug:
    print('SCORES', scores_sort)
    print('SORTED', dict(sorted(scores_sort.items(), key=operator.itemgetter(0))))
    print('SORTED2', dict(sorted(scores_sort.items(), key=operator.itemgetter(1))))

  return scores_sort


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
