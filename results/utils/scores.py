import matplotlib.pyplot as plt
import requests
import boto3
import json

def get_results(stocks, debug=False, category=0, total_money=1000):
  results = {}
  total_parts = 0

  for stock, v in stocks.items():
    stock_parts = 0
    results[stock] = {}
    results[stock]['category'] = v['category']
    if v['category'] == category or category == '0' and v['category'] != '6':
      if v['score'] < -75:
        results[stock]['parts'] = 0
        stock_parts = stock_parts + 0
      elif v['score'] < -50:
        results[stock]['parts'] = 1
        stock_parts = stock_parts + 1
      elif v['score'] < -25:
        results[stock]['parts'] = 2
        stock_parts = stock_parts + 2
      elif v['score'] < 0:
        results[stock]['parts'] = 3
        stock_parts = stock_parts + 3
      elif v['score'] < 25:
        results[stock]['parts'] = 4
        stock_parts = stock_parts + 4
      elif v['score'] < 50:
        results[stock]['parts'] = 5
        stock_parts = stock_parts + 5
      elif v['score'] < 75:
        results[stock]['parts'] = 6
        stock_parts = stock_parts + 6
      elif v['score'] >= 75:
        results[stock]['parts'] = 7
        stock_parts = stock_parts + 7
      else:
        raise Exception("Invalid Stock Score: " + str(stock) + ' - ' + str(v['score']))

    total_parts = total_parts + stock_parts

  money_per_part = total_money / total_parts
  results['total_money'] = total_money
  results['total_parts'] = total_parts
  results['money_per_part'] = round(money_per_part, 2)

  ordered = []
  for stock, v in stocks.items():
    if v['category'] == category or category == '0' and v['category'] != '6':
      results[stock]['cash'] = round(money_per_part * results[stock]['parts'], 2)
      results[stock]['shares'] = round(results[stock]['cash'] / v['current_price'], 4)
      results[stock]['price'] = round(v['current_price'], 2)
      ordered.append({'parts': results[stock]['parts'],
                      'stock': stock,
                      'shares': results[stock]['shares'], 
                      'score': v['score'],
                      'cash': results[stock]['cash'],
                      'price': results[stock]['price']})

  return results, sorted(ordered, key=lambda d: d['score'])


def get_scores_list(api='http://2030.hex7.com/scores/',
                    bucket='2030.hex7.com',
                    prefix='scores',
                    debug=False):
  s_list = []
  client = boto3.client("s3", region_name='us-east-1')
  response = client.list_objects_v2(Bucket=bucket,
                                    Prefix=prefix,
                                    Delimiter='/')

  if 'Contents' not in response:
        raise Exception('response', response)

  else:
    for key in response['Contents']:
        s_list.append(key['Key'])

  if debug:
    print('s_list: ', s_list)

  return s_list


def get_matrix(scores, debug=False, bucket='2030.hex7.com'):
  matrix = {}
  if debug:
    print('scores', scores)

  for key in scores:
    req = 'http://' + bucket + '/' + key

    r = requests.get(req)
    #if r.status_code != 200:
    #  raise Exception("req: ", req, "status code: ", r.status_code)

    r_dict = json.loads(r.text)
    if debug:
      print('key', key)
      print('req', req)
      print('r_dict', r_dict)

    for k, v in r_dict.items():
      if k in matrix:
        matrix[k].append(round(v['score'], 2))
      else:
        matrix[k] = []
        matrix[k].append(round(v['score'], 2))

    if debug:
      print('matrix', matrix)

    return matrix


def make_charts(matrix, savepath='static/', debug=False):
  for stock, s in matrix.items():
    if debug:
      print('stock: ', stock)
      print('scores: ', s)

    plt.ticklabel_format(useOffset=False, style='plain')
    plt.title(stock + ' scores')
    plt.xlabel('time')
    plt.ylabel('scores')
    plt.plot(s, color="green")
    plt.savefig(savepath + stock + '-scores.png')
    plt.close()
