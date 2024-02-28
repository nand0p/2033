

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
        r[s]['catname'] = 'Cloud Stocks'
      elif v == '3':
        r[s]['catname'] = 'ETF'
      elif v == '4':
        r[s]['catname'] = 'BioTech'
      elif v == '5':
        r[s]['catname'] = 'Sustainable Future'
      elif v == '6':
        r[s]['catname'] = 'Crypto'
      elif v == '7':
        r[s]['catname'] = 'Asia Emerging'
      elif v == '8':
        r[s]['catname'] = 'Cloud Growth'
      else:
        r[s]['catname'] = 'None'

  return r
