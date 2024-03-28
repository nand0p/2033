from argparse import ArgumentParser
from prettytable import PrettyTable
import requests
import json


parser = ArgumentParser()
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('--verbose', action='store_true', help='verbose')
parser.add_argument('--out', action='store_true', help='out')
parser.add_argument('--all', action='store_true', help='set all flags true')
parser.add_argument('--exclude', action='store_true', help='excluded stocks')
parser.add_argument('--include', action='store_true', help='included stocks')
parser.add_argument('--toxic', action='store_true', help='excluded stocks')
parser.add_argument('--speed', type=str, default='slow', help='fast or slow')
parser.add_argument('--savefile', type=str, default='buy.json', help='json out file')
parser.add_argument('--money', type=int, default=25, help='fast or slow')
parser.add_argument('--limit', type=int, default=100, help='max stock price')
args = parser.parse_args()

if args.all:
    args.verbose = True
    args.exclude = True
    args.include = True
    args.toxic = True
    args.out = True

s = {}
buy = []
count = 0
total = 0
toxic = []
include = []
exclude = []
total_parts = 0

headers = [ 'count',
            'stock',
            'shares',
            'cash',
            'parts',
            'price' ]

r = requests.get('http://localhost/' + args.speed + '_ordered')
results = json.loads(r.text)

if args.debug:
  print(results)
else:
  print('status: ', r.status_code)

for stocks in results:
  if args.debug:
    print(type(stocks))
    print(stocks)

  current = stocks['stock']
  s[current] = {}

  for key, value in stocks.items():
    if key == 'shares':
      if value > 0:
        if value < 1:
          s[current]['shares'] = 1
        else:
          s[current]['shares'] = int(value)

    if key == 'parts':
      s[current]['parts'] = value

    if key == 'price':
      if 'shares' in s[current]:
        s[current]['price'] = value


print()
print('Whole Share Strategy Generator')
print()

table = PrettyTable(headers)
for key, value in s.items():
  if value['parts'] > 0:
    if value['price'] < args.limit:
      x = value['parts'] * args.money
      shares = int(x / value['price'])
      if shares > 0 or args.toxic:
        include.append(key)
        cash = round(shares * value['price'], 2)
        total = total + cash
        count = count + 1
        total_parts = total_parts + value['parts']
        if shares > 0:
          table.add_row([count,
                         key,
                         shares,
                         cash,
                         value['parts'],
                         value['price']])
          buy.append({key: [shares, value['price']]})
        else:
          toxic.append(key)

        if args.debug:
          print('x: ', x)
          print('current: ', total)
          print('count: ', count)
          print('stock: ',  key)
          print('shares: ', shares)
          print('cash: ', cash)
          print('parts: ', value['parts'])
          print('price: ', value['price'])
      else:
        exclude.append(key)
    else:
      exclude.append(key)

if args.verbose:
  print(table)

if args.include:
  print('Included: ', include)

if args.exclude:
  print('Excluded: ', exclude)

if args.toxic:
  print('Toxic: ', toxic)

if args.out:
  print()
  print('Buy: ', buy)

with open(args.savefile, 'w') as f:
    json.dump(buy, f)

print()
print('total stocks: ', count)
print('total parts: ', total_parts)
print('money per part: ', args.money)
print('total cash: ', round(total, 2))
print()
