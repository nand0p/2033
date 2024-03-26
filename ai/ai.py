
stock_file = 'ai.004.txt'
master_file = '2030.txt'
debug = False
stocks = []
missing = []

with open(stock_file) as file:
    s = file.readlines()
with open(master_file) as file:
    m = file.readlines()

if debug:
  print('stock_file', s)
  print('master_file', m)

for item in s:
  if '$' in item:
    ticker = item.split('$')[-1].strip()

    if debug:
      print('item: ', item)
      print('saving: ', ticker)

    if ticker:
      stocks.append(ticker)

    found = False
    for master in m:
      if ticker in master:
        found = True

    if not found:
      missing.append(ticker)

print(stock_file, ': ', stocks)
print('missing: ', missing)
