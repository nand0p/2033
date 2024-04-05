from ib_insync import IB, Stock, Contract, Ticker
from argparse import ArgumentParser
from pprint import pprint
import json
import re


parser = ArgumentParser()
parser.add_argument('--port', type=int, default=4001)
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--client', type=int, default=1)
parser.add_argument('--ticker', type=str, default='AAPL')
parser.add_argument('--start', type=str, default='20240101 00:00:00')
parser.add_argument('--end', type=str, default='')
parser.add_argument('--codes', type=str, default='BRFG+BRFUPDN+DJNL')
parser.add_argument('--results', type=int, default=100)
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()


ib = IB()

print('connect')
conn = ib.connect(host=args.host,
                  port=args.port,
                  clientId=args.client,
                  timeout=5)
pprint(conn)


with open('../2033.txt') as f:
    lines = f.readlines()

stocks = {}
for line in lines:
  r = line.split(':')
  if r[0].isalpha() and r[0] != 'fbiox':
    stocks[r[0]] = r[1].strip()

n = []
for s_key, category in stocks.items():
  stock = Stock(symbol=s_key, exchange='SMART', currency='USD')
  stock_out = ib.qualifyContracts(stock)
  conId = stock_out[0].conId

  if args.debug:
    print('stock: ', s_key)
    print('conId: ', conId)

  news = ib.newsBulletins()
  r_news = ib.reqHistoricalNews(conId,
                                providerCodes=args.codes,
                                startDateTime=args.start,
                                endDateTime=args.end,
                                totalResults=args.results);

  for n_key in r_news:
    t = n_key.time.isoformat()
    val = s_key + ':' + category + ':' + n_key.headline.split('}')[1] + ':' + t + ':'
    if '2024' in t:
      n.append(val)
      if args.debug:
        print(val)


with open("news.json", "w") as f:
    f.write(json.dumps(n))
