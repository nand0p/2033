from pprint import pprint
import requests
import json


debug = False
speed = 'fast'


if speed == 'fast':
  r = requests.get('http://localhost/fast_ordered')
  results = json.loads(r.text)

elif speed == 'slow':
  r = requests.get('http://localhost/slow_ordered')
  results = json.loads(r.text)

else:
  raise Exception('set speed variable')


if debug:
  pprint(type(results))
  pprint(results)

s = {}
total = 0
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
for key, value in s.items():
  if len(value) > 0:
    final.append({key: value})

    money = round(value.get('shares', 0) * value.get('price', 0), 2)
    if money > 0:
      total = total + money

pprint(final)

print()
print('total cash: ', round(total, 2))
