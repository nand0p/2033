import matplotlib.pyplot as plt
import requests
import unittest
import json
import os

def get_results(stocks,
                source_file,
                debug=False,
                category='0',
                total_money=1000):

  results = {}
  total_parts = 0

  with open(source_file, 'r') as file:
    source = file.read().replace('\n', '').upper()

  for stock, v in stocks.items():
    if stock in source:
      stock_parts = 0
      results[stock] = {}
      results[stock]['category'] = v['category']

      if v['category'] == category or \
         v['category'] != '6' and \
         category == '0':

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
    if stock in source:
      if v['category'] == category or \
         v['category'] != '6' and \
         category == '0':

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


def get_scores_list(api='http://2030.hex7.com/',
                    scores_file='scores_list.json',
                    debug=False):

  url = api + scores_file
  r = requests.get(url)
  scores_list = json.loads(r.text)

  if debug:
    print(scores_list)

  return scores_list


def make_charts(matrix,
                savepath='static/',
                debug=False):

  slow = {}
  fast = {}

  for speed, v in matrix.items():
    for stock, s in v.items():
      if speed == 'slow':
        if isinstance(s, dict):
          slow[stock] = s['scores']
      elif speed == 'fast':
        if isinstance(s, dict):
          fast[stock] = s['scores']

  for slow_stock, slow_scores in slow.items():
    for fast_stock, fast_scores in fast.items():
      if slow_stock == fast_stock:
        while len(slow_scores) != len(fast_scores):
          fast_scores.insert(0, fast_scores[0])

  for stock in slow.keys():
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.xlabel('time')
    plt.ylabel('scores')
    plt.title(stock + ' scores')
    plt.ylim(-100, 100)
    plt.plot(slow[stock], color='red')
    plt.plot(fast[stock], color='green')
    plt.savefig(savepath + stock + '-scores.png')
    plt.close()


def save_scores(matrix,
                slow_results,
                fast_results,
                savepath,
                scores_key,
                bucket='2030.hex7.com',
                save_to_s3=False,
                debug=False):

  if save_to_s3:
    s3 = boto3.resource('s3')
    s3_matrix = s3.Object(bucket, scores_key)
    s3_matrix.put(Body=(bytes(json.dumps(matrix).encode('UTF-8'))),
                  ACL='public-read')

    s3_slow_results = s3.Object(bucket, 'results_slow.json')
    s3_slow_results.put(Body=(bytes(json.dumps(slow_results).encode('UTF-8'))),
                        ACL='public-read')

    s3_fast_results = s3.Object(bucket, 'results_fast.json')
    s3_fast_results.put(Body=(bytes(json.dumps(fast_results).encode('UTF-8'))),
                        ACL='public-read')

  if not os.path.exists(savepath):
    print('Making savepath: ' + savepath)
    os.makedirs(savepath)

  with open(savepath + scores_key, 'w') as out:
    json.dump(matrix, out, ensure_ascii=True, indent=4)


def get_matrix(s_list,
               slow_results,
               fast_results,
               source_file='2030.txt',
               bucket='2030.hex7.com',
               category='0',
               debug=False):

  matrix = {}
  matrix['slow'] = {}
  matrix['fast'] = {}

  with open(source_file, 'r') as file:
    source = file.read().replace('\n', '').upper()

  for key in s_list:
    req = 'http://' + bucket + '/' + key
    r = requests.get(req)
    r_dict = json.loads(r.text)

    for k, v in r_dict.items():
      if k in source:
        if k not in matrix['fast']:
          matrix['fast'][k] = {}
          matrix['fast'][k]['scores'] = []

        elif k not in matrix['slow']:
          matrix['slow'][k] = {}
          matrix['slow'][k]['scores'] = []

        if slow_results[k]['category'] == category or \
           slow_results[k]['category'] != '6' and \
           category == '0':

          if 'fast' in key:
            matrix['fast'][k]['scores'].append(round(v['score'], 2))

          else:
            matrix['slow'][k]['scores'].append(round(v['score'], 2))

  fast_count = 0
  for stock in matrix['slow'].keys():
    if 'parts' not in matrix['fast']:
      matrix['fast']['parts'] = 0
      matrix['fast']['total_parts'] = 0
      matrix['fast']['parts1'] = 0
      matrix['fast']['parts2'] = 0
      matrix['fast']['parts3'] = 0
      matrix['fast']['parts4'] = 0
      matrix['fast']['parts5'] = 0
      matrix['fast']['parts6'] = 0
      matrix['fast']['parts7'] = 0

    if 'parts' not in stock:
      if fast_results[stock].get('parts', 0) > 0:
        fast_count = fast_count + 1
        matrix['fast']['parts'] += fast_results[stock].get('price', 0)
        matrix['fast']['total_parts'] += fast_results[stock].get('price', 0) * fast_results[stock].get('parts', 0)
        if fast_results[stock].get('parts', 0) > 1:
          matrix['fast']['parts1'] += fast_results[stock].get('price', 0)
        if fast_results[stock].get('parts', 0) > 2:
          matrix['fast']['parts2'] += fast_results[stock].get('price', 0)
        if fast_results[stock].get('parts', 0) > 3:
          matrix['fast']['parts3'] += fast_results[stock].get('price', 0)
        if fast_results[stock].get('parts', 0) > 4:
          matrix['fast']['parts4'] += fast_results[stock].get('price', 0)
        if fast_results[stock].get('parts', 0) > 5:
          matrix['fast']['parts5'] += fast_results[stock].get('price', 0)
        if fast_results[stock].get('parts', 0) > 6:
          matrix['fast']['parts6'] += fast_results[stock].get('price', 0)
        if fast_results[stock].get('parts', 0) > 7:
          matrix['fast']['parts7'] += fast_results[stock].get('price', 0)

  slow_count = 0
  for stock in matrix['fast'].keys():
    if 'parts' not in matrix['slow']:
      matrix['slow']['parts'] = 0
      matrix['slow']['total_parts'] = 0
      matrix['slow']['parts1'] = 0
      matrix['slow']['parts2'] = 0
      matrix['slow']['parts3'] = 0
      matrix['slow']['parts4'] = 0
      matrix['slow']['parts5'] = 0
      matrix['slow']['parts6'] = 0
      matrix['slow']['parts7'] = 0

    if 'parts' not in stock:
      if slow_results[stock].get('parts', 0) > 0:
        slow_count = slow_count + 1
        matrix['slow']['parts'] += slow_results[stock].get('price', 0)
        matrix['slow']['total_parts'] += slow_results[stock].get('price', 0) * slow_results[stock].get('parts', 0)
        if slow_results[stock].get('parts', 0) > 1:
          matrix['slow']['parts1'] += slow_results[stock].get('price', 0)
        if slow_results[stock].get('parts', 0) > 2:
          matrix['slow']['parts2'] += slow_results[stock].get('price', 0)
        if slow_results[stock].get('parts', 0) > 3:
          matrix['slow']['parts3'] += slow_results[stock].get('price', 0)
        if slow_results[stock].get('parts', 0) > 4:
          matrix['slow']['parts4'] += slow_results[stock].get('price', 0)
        if slow_results[stock].get('parts', 0) > 5:
          matrix['slow']['parts5'] += slow_results[stock].get('price', 0)
        if slow_results[stock].get('parts', 0) > 6:
          matrix['slow']['parts6'] += slow_results[stock].get('price', 0)
        if slow_results[stock].get('parts', 0) > 7:
          matrix['slow']['parts7'] += slow_results[stock].get('price', 0)

  matrix['slow']['count'] = slow_count
  matrix['slow']['parts'] = round(matrix['slow']['parts'], 2)
  matrix['slow']['total_parts'] = round(matrix['slow']['total_parts'], 2)
  matrix['fast']['count'] = fast_count
  matrix['fast']['parts'] = round(matrix['fast']['parts'], 2)
  matrix['fast']['total_parts'] = round(matrix['fast']['total_parts'], 2)

  return matrix


def get_url(url, debug=False):
  r = requests.get(url)

  if r.status_code != 200:
    raise Exception("req: ", url, " status code: ", r.status_code)

  return json.loads(r.text)
