def get_min_shares(stocks, debug=False, category=0, total_money=1000):
  share_one = 0

  for stock, v in stocks.items():
    if v['category'] == category or category == '0':
      share_one += v['current_price']

  return round(share_one, 2)
