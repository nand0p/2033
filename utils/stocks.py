import json

def get_categories(catfile):

  with open(catfile, 'r') as f:
    categories = json.load(f)

  return categories



def get_stocks(stocks, cat, categories):
  r = {}
  stocks = sorted(set(stocks.strip('\"').upper().split()))

  for stock in stocks:
      s, v = stock.split(':')
      if v == cat or cat == '0':
          r[s] = {}
          r[s]['category'] = cat
          r[s]['catname'] = categories[int(v)] if v in categories else 'None'

  return r
