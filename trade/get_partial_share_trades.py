from jinja2 import Environment, FileSystemLoader, Template
from argparse import ArgumentParser
from datetime import datetime
from zoneinfo import ZoneInfo
from pprint import pprint
import requests
import boto3
import json
import os


parser = ArgumentParser()
parser.add_argument('--host', type=str, default='localhost', help='show account values')
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('--money', type=int, default=1000, help='cash to buy')
parser.add_argument('--category', type=int, default=0, help='category 1-8')
parser.add_argument('--outfile', type=str, default='results.html', help='out file')
parser.add_argument('--outdir', type=str, default='./tmp/', help='out directory')
parser.add_argument('--bucket', type=str, default='2030.hex7.com', help='s3 bucket')
args = parser.parse_args()

extra_args = {'ACL': 'public-read',
              'ContentType': 'text/html',
              'ContentLanguage': 'en-US'}

datemade = ' - '.join(datetime.now(ZoneInfo('US/Eastern')).isoformat().split('T'))

if args.debug:
  print(r.text)


url = 'http://' + args.host + '?cat=' + str(args.category) + '&cash=' + str(args.money)
print('get current results: ' + url)
r = requests.get(url)
if r.status_code == 200:
  print('success: ', r.status_code)
else:
  raise Exception('API not available: ' + url)


url = 'http://' + args.host + '/slow_ordered'
print('parse slow results: ' + url)
r_slow = requests.get(url)
if r_slow.status_code == 200:
  print('success: ', r_slow.status_code)
else:
  raise Exception('API not available: ' + url)


url = 'http://' + args.host + '/fast_ordered'
print('parse fast results: ' + url)
r_fast = requests.get('http://' + args.host + '/fast_ordered')
if r_fast.status_code == 200:
  print('success: ', r_fast.status_code)
else:
  raise Exception('API not available: ' + url)


fast_results = json.loads(r_fast.text)
slow_results = json.loads(r_slow.text)


if args.debug:
  pprint(type(fast_results))
  pprint(fast_results)
  pprint(type(slow_results))
  pprint(slow_results)


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
  pprint(final)
  print('total cash fast: ', round(total_fast, 2))
  print('total cash slow: ', round(total_slow, 2))


print('render jinja')
j2_file_loader = FileSystemLoader('templates')
j2_env = Environment(loader=j2_file_loader)
j2_template = j2_env.get_template(args.outfile)
j2_rendered = j2_template.render(slow_final=slow_final,
                                 fast_final=fast_final,
                                 datemade=datemade,
                                 total_slow=round(total_slow, 2),
                                 total_fast=round(total_fast, 2))

if args.debug:
  print(j2_rendered)


filename = args.outdir + args.outfile
outslow = args.outdir + 'slow_final.json'
outfast = args.outdir + 'fast_final.json'
print('save: ', filename)
print('save: ', outslow)
print('save: ', outfast)
if not os.path.exists(args.outdir):
  os.makedirs(args.outdir)
with open(filename, 'w') as f:
  f.write(j2_rendered)
with open(outslow, 'w') as f:
  json.dump(slow_final, f)
with open(outfast, 'w') as f:
  json.dump(fast_final, f)


print('upload to s3')
s3_client = boto3.client('s3')
s3_client.upload_file(Filename=filename,
                      Bucket=args.bucket,
                      Key=args.outfile,
                      ExtraArgs=extra_args)
