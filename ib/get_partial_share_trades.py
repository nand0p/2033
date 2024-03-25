from pprint import pprint
import requests
import json


debug = True

r_fast = requests.get('http://localhost/fast_ordered')
results_fast = json.loads(r_fast.text)

r_slow = requests.get('http://localhost/slow_ordered')
results_slow = json.loads(r_slow.text)

if debug:
  pprint(type(results_fast))
  pprint(results_fast)
  pprint(type(results_slow))
  pprint(results_slow)

s = {}
total = 0
for stocks in results_fast:
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
for key, value in s.items():
  if len(value) > 0:
    final.append({key: value})

    money = round(value.get('shares', 0) * value.get('price', 0), 2)
    if money > 0:
      total = total + money

pprint(final)

print()
print('total cash: ', round(total, 2))
