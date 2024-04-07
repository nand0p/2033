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
parser.add_argument('--fast', action='store_true', help='stocks for fast')
parser.add_argument('--slow', action='store_true', help='stocks for slow')
parser.add_argument('--skip-init', action='store_true', help='skip initialization')
parser.add_argument('--outdir', type=str, default='./tmp/', help='out directory')
parser.add_argument('--money', type=int, default=25, help='money per part')
parser.add_argument('--limit', type=int, default=100, help='max stock price')
parser.add_argument('--category', type=int, default=2, help='stock category')
parser.add_argument('--savefile', type=str, help='json out file')
args = parser.parse_args()

if args.all:
  args.verbose = True
  args.toxic = True
  args.out = True

if args.fast:
  if not args.savefile:
    args.savefile = 'buy_whole_fast_cat' + str(args.category) + '.json'
elif args.slow:
  if not args.savefile:
    args.savefile = 'buy_whole_slow_cat' + str(args.category) + '.json'
else:
  raise Exception('please specify --fast or --slow')

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

if not args.skip_init:
  init = 'http://localhost/?cat=' + str(args.category)
  print('hit results api: ', init)
  q = requests.get(init)
  if q.status_code != 200:
    raise Exception('cannot hit url: ' + init)

if args.fast:
  url = 'http://localhost/fast_ordered'
elif args.slow:
  url = 'http://localhost/slow_ordered'

print('get results data: ' + url)
r = requests.get(url)
if r.status_code != 200:
  raise Exception('cannot hit url: ' + url)
results = json.loads(r.text)

if args.debug:
  print(results)
else:
  print('status: ', r.status_code)

print('process results')
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

      if shares > 0:
        include.append(key)
        cash = round(shares * value['price'], 2)
        total = total + cash
        count = count + 1
        total_parts = total_parts + value['parts']
        table.add_row([count,
                       key,
                       shares,
                       cash,
                       value['parts'],
                       value['price']])
        buy.append([key, shares, value['price']])

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
  else:
    toxic.append(key)


print(table)

if args.include or args.verbose:
  print('Included: ', include)

if args.exclude or args.verbose:
  print('Excluded: ', exclude)

if args.toxic or args.verbose:
  print('Toxic: ', toxic)

if args.verbose:
  print('\nBuy: ', buy)

if args.out:
  print('\njson dir: ', args.outdir, '\njson file: ', args.savefile)
  with open(args.outdir + args.savefile, 'w') as f:
      json.dump(buy, f)
  with open('buy.json', 'w') as f:
      json.dump(buy, f)

print()
print('total stocks: ', count)
print('total parts: ', total_parts)
print('money per part: ', args.money)
print('total cash: ', round(total, 2))
print()
