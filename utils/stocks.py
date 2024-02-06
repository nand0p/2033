

def get_stocks(stocks, cat):
  stocks = sorted(set(stocks.strip('\"').upper().split()))
  r = {}

  for stock in stocks:
    s, v = stock.split(':')
    if v == cat or cat == '0':
      r[s] = {}
      r[s]['category'] = v

  return r
