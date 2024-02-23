

def get_stocks(stocks, cat):
  stocks = sorted(set(stocks.strip('\"').upper().split()))
  r = {}

  for stock in stocks:
    s, v = stock.split(':')
    if v == cat or cat == '0':
      r[s] = {}
      r[s]['category'] = v
      if v == '1':
        r[s]['catname'] = 'Cloud XL'
      elif v == '2':
        r[s]['catname'] = 'Cloud Stock'
      elif v == '3':
        r[s]['catname'] = 'ETF'
      elif v == '4':
        r[s]['catname'] = 'BioTech'
      elif v == '5':
        r[s]['catname'] = 'Sustainable Future'
      elif v == '6':
        r[s]['catname'] = 'Crypto'
      else:
        r[s]['catname'] = 'None'

  return r


def get_results(stocks, debug, total_money=1000):
  results = {}
  total_parts = 0

  for stock, value in stocks.items():
    stock_parts = 0
    results[stock] = {}
    if value['score_color'] == 'red':
      results[stock]['parts'] = 1
      stock_parts = stock_parts + 1
    elif value['score_color'] == 'yellow':
      results[stock]['parts'] = 2
      stock_parts = stock_parts + 2
    elif value['score_color'] == 'green':
      results[stock]['parts'] = 4
      stock_parts = stock_parts + 4
    total_parts = total_parts + stock_parts

  money_per_part = total_money / total_parts
  results['total_money'] = total_money
  results['total_parts'] = total_parts
  results['money_per_part'] = round(money_per_part, 2)

  for stock, value in stocks.items():
    results[stock]['cash'] = round(money_per_part * results[stock]['parts'], 2)
    results[stock]['shares'] = round(value['current_price'] / results[stock]['cash'], 4)

  return results
