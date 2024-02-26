from operator import itemgetter

def get_results(stocks, debug=False, category=0, total_money=1000):
  results = {}
  total_parts = 0

  for stock, v in stocks.items():
    stock_parts = 0
    results[stock] = {}
    if v['category'] == category or category == '0':
      if v['score'] < -33:
        results[stock]['parts'] = 1
        stock_parts = stock_parts + 1
      elif v['score'] < 0:
        results[stock]['parts'] = 2
        stock_parts = stock_parts + 2
      elif v['score'] < 33:
        results[stock]['parts'] = 3
        stock_parts = stock_parts + 3
      elif v['score'] < 66:
        results[stock]['parts'] = 5
        stock_parts = stock_parts + 5
      elif v['score'] >= 66:
        results[stock]['parts'] = 8
        stock_parts = stock_parts + 8
      else:
        raise Exception("Invalid Stock Score: " + str(stock) + ' - ' + str(v['score']))

    total_parts = total_parts + stock_parts

  money_per_part = total_money / total_parts
  results['total_money'] = total_money
  results['total_parts'] = total_parts
  results['money_per_part'] = round(money_per_part, 2)

  ordered = []
  for stock, v in stocks.items():
    if v['category'] == category or category == '0':
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
