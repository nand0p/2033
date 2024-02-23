import matplotlib
import datetime
import operator
import boto3    
import json


save_to_s3 = False
s3 = boto3.resource('s3')
bucket = '2030.hex7.com'
date = datetime.datetime.now().isoformat().split('T')[0]
scores_key = 'scores-' + date + '.json'


def save_scores(stocks, data_dir, debug=False):
  scores_out = {}
  for stock in stocks.keys():
    scores_out[stock] = stocks[stock]['score']
    if debug:
      print('scores', stock, scores_out[stock])

  with open(data_dir + scores_key, 'w') as out:
    json.dump(scores_out, out, ensure_ascii=True, indent=4)

  if save_to_s3:
    s3object = s3.Object(bucket, scores_key)
    s3object.put(Body=(bytes(json.dumps(scores).encode('UTF-8'))))

  scores_sort = {}
  for stock in stocks.keys():
    score = round(stocks[stock]['score'], 3)
    if score > 100:
      score = 99.999
    elif score < -100:
      score = -99.999
    scores_sort.update({score: stock})

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
