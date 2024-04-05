from jinja2 import Environment, FileSystemLoader, Template
from prettytable import PrettyTable
from argparse import ArgumentParser
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import boto3
import json
import os


parser = ArgumentParser()
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('--verbose', action='store_true', help='verbose')
parser.add_argument('--upload-to-s3', action='store_true', help='upload to s3')
parser.add_argument('--generate-html', action='store_true', help='generate html')
parser.add_argument('--all', action='store_true', help='set all flags true')
parser.add_argument('--exclude', action='store_true', help='excluded stocks')
parser.add_argument('--include', action='store_true', help='included stocks')
parser.add_argument('--fast', action='store_true', help='run on fast')
parser.add_argument('--slow', action='store_true', help='run on slow')
parser.add_argument('--host', type=str, default='localhost', help='show account values')
parser.add_argument('--money', type=int, default=1000, help='cash to buy')
parser.add_argument('--category', type=int, default=0, help='category 1-8')
parser.add_argument('--outfile', type=str, default='results.html', help='out file')
parser.add_argument('--outdir', type=str, default='./tmp/', help='out directory')
parser.add_argument('--bucket', type=str, default='2033.hex7.com', help='s3 bucket')
parser.add_argument('--savefile_fast', type=str, help='json out file')
parser.add_argument('--savefile_slow', type=str, help='json out file')
args = parser.parse_args()


if args.all:
  args.fast = True
  args.slow = True
  args.verbose = True
  args.exclude = True
  args.include = True
  args.upload_to_s3 = True
  args.generate_html = True

if not args.fast and not args.slow:
  raise Exception('please use --fast, --slow, or --all')

if not args.savefile_fast:
  args.savefile_fast = 'buy_partial_fast_cat' + str(args.category) + '.json'
if not args.savefile_slow:
  args.savefile_slow = 'buy_partial_slow_cat' + str(args.category) + '.json'


datemade = ' - '.join(datetime.now(ZoneInfo('US/Eastern')).isoformat().split('T'))
extra_args = {'ACL': 'public-read',
              'ContentType': 'text/html',
              'ContentLanguage': 'en-US'}
if args.debug:
  print('datemade: ', datemade)
  print('extra_args: ', extra_args)


url = 'http://' + args.host + '?cat=' + str(args.category) + '&cash=' + str(args.money)
print('get current results: ' + url)
r = requests.get(url)
if r.status_code == 200:
  print('success: ', r.status_code)
else:
  raise Exception('API not available: ' + url)
if args.debug:
  print(r.text)


url = 'http://' + args.host + '/slow_ordered'
print('parse slow results: ' + url)
r_slow = requests.get(url)
if r_slow.status_code == 200:
  print('success: ', r_slow.status_code)
else:
  raise Exception('API not available: ' + url)
slow_results = json.loads(r_slow.text)
if args.debug:
  print('r_slow: ', r_slow.text)
  print('slow_results: ', slow_results)


url = 'http://' + args.host + '/fast_ordered'
print('parse fast results: ' + url)
r_fast = requests.get('http://' + args.host + '/fast_ordered')
if r_fast.status_code == 200:
  print('success: ', r_fast.status_code)
else:
  raise Exception('API not available: ' + url)
fast_results = json.loads(r_fast.text)
if args.debug:
  print('r_fast: ', r_fast.text)
  print('fast_results: ', fast_results)


def get_stocks(results, debug):
  s = {}
  for stocks in results:
    if debug:
      print(type(stocks))
      print(stocks)

    current = stocks['stock']
    s[current] = {}

    for key, value in stocks.items():
      if key == 'shares':
        if value > 0:
          s[current]['shares'] = value

      if key == 'price':
        if 'shares' in s[current]:
          s[current]['price'] = value

  for key, value in s.items():
    if value:
      if debug:
        print('key: ', key)
        print('value: ', value)
      s[key]['cash'] = round(value['shares'] * value['price'], 2)

  final = []
  total = 0
  for key, value in s.items():
    if len(value) > 0:
      final.append({key: value})
      money = round(value.get('shares', 0) * value.get('price', 0), 2)
      if money > 0:
        total = total + money

  return final, total


print('generate final slow results')
slow_final, total_slow = get_stocks(slow_results, args.debug)
print('generate final fast results')
fast_final, total_fast = get_stocks(fast_results, args.debug)
if args.debug:
  print('fast_final: ', fast_final)
  print('total_fast: ', total_fast)
  print('slow_final: ', slow_final)
  print('total_slow: ', total_slow)


if args.generate_html:
  print('render jinja: ', args.outfile)
  j2_file_loader = FileSystemLoader('templates')
  j2_env = Environment(loader=j2_file_loader)
  j2_template = j2_env.get_template(args.outfile)
  j2_rendered = j2_template.render(slow_final=slow_final,
                                   fast_final=fast_final,
                                   datemade=datemade,
                                   total_slow=round(total_slow, 2),
                                   total_fast=round(total_fast, 2))

  if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)
  with open(args.outdir + args.outfile, 'w') as f:
    f.write(j2_rendered)

  if args.debug:
    print('html: ', j2_rendered)
    print('save: ', filename)


if args.fast:
  r = []
  fast = PrettyTable(['Stock', 'Shares', 'Price'])
  for p in fast_final:
    for stock, q in p.items():
      fast.add_row([stock, q['shares'], q['price']])
      r.append([stock, q['shares'], q['price']])
  with open(args.outdir + args.savefile_fast, 'w') as f:
    json.dump(r, f)
  with open('buy.json', 'w') as f:
    json.dump(r, f)
  print()
  print(fast)
  print()
  print(r)
  print()
  print('savedir: ', args.outdir)
  print('savefile: ', args.savefile_fast)
  print('total cash fast: ', round(total_fast, 2))
  print()


if args.slow:
  r = []
  slow = PrettyTable(['Stock', 'Shares', 'Price'])
  for p in slow_final:
    for stock, q in p.items():
      slow.add_row([stock, q['shares'], q['price']])
      r.append([stock, q['shares'], q['price']])
  with open(args.outdir + args.savefile_slow, 'w') as f:
    json.dump(r, f)
  with open('buy.json', 'w') as f:
    json.dump(r, f)
  print()
  print(slow)
  print()
  print(r)
  print()
  print('savedir: ', args.outdir)
  print('savefile: ', args.savefile_slow)
  print('total cash slow: ', round(total_slow, 2))
  print()


if args.upload_to_s3:
  print('upload to s3: ', args.bucket, '\n-------> key: ', args.outfile)
  s3_client = boto3.client('s3')
  file_local = args.outdir + args.outfile
  s3_client.upload_file(Filename=file_local,
                        Bucket=args.bucket,
                        Key=args.outfile,
                        ExtraArgs=extra_args)
