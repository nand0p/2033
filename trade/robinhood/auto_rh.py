import robin_stocks.robinhood as rh
from prettytable import PrettyTable
from argparse import ArgumentParser
from pprint import pprint
import json
import os


parser = ArgumentParser()
parser.add_argument('--pause', type=int, default=1, help='sleep iteration')
parser.add_argument('--robin-user', type=str, default=os.environ.get('ROBINHOOD_USER'), help='robinhood username')
parser.add_argument('--robin-pass', type=str, default=os.environ.get('ROBINHOOD_PASS'), help='robinhood password')
parser.add_argument('--ticker', type=str, help='ticker to execute')
parser.add_argument('--buy-file', type=str, default='../buy.json', help='file to execute')
parser.add_argument('--shares', type=int, help='shares')
parser.add_argument('--price', type=float, help='price')
parser.add_argument('--account-summary', action='store_true', help='show account summary')
parser.add_argument('--orders', action='store_true', help='show orders')
parser.add_argument('--balances', action='store_true', help='show account balances')
parser.add_argument('--portfolio', action='store_true', help='show portfolio')
parser.add_argument('--positions', action='store_true', help='show positions')
parser.add_argument('--transactions', action='store_true', help='show transactions')
parser.add_argument('--dividends', action='store_true', help='show dividends')
parser.add_argument('--earnings', action='store_true', help='show earnings')
parser.add_argument('--events', action='store_true', help='show events')
parser.add_argument('--fundamentals', action='store_true', help='show fundamentals')
parser.add_argument('--news', action='store_true', help='show news')
parser.add_argument('--ratings', action='store_true', help='show ratings')
parser.add_argument('--order-shares', action='store_true', help='order by shares')
parser.add_argument('--order-cash', action='store_true', help='order by total cash')
parser.add_argument('--extended-hours', action='store_true', help='execute during extended hours')
parser.add_argument('--logout', action='store_true', help='terminate robinhood session')
parser.add_argument('--query', action='store_true', help='query mode')
parser.add_argument('--query-string', type=str, help='query string to execute')
parser.add_argument('--crypto', action='store_true', help='execute crypto order')
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('--verbose', action='store_true', help='verbose output')
parser.add_argument('--all', action='store_true', help='store all true')
parser.add_argument('--confirm', action='store_true', help='flag required to execute trade')

buy_type = parser.add_mutually_exclusive_group(required=False)
buy_type.add_argument('--buy-file-market', action='store_true', help='execute buy from file')
buy_type.add_argument('--buy-file-limit', action='store_true', help='execute buy from file')
buy_type.add_argument('--buy-single-market', action='store_true', help='execute market buy from ticker arg')
buy_type.add_argument('--buy-single-limit', action='store_true', help='execute limit buy from ticker arg')
args = parser.parse_args()


if args.all:
  args.balances = True
  args.portfolio = True
  args.account_summary = True
  args.ratings = True
  args.fundamentals = True
  args.news = True
  args.events = True
  args.earnings = True


if args.debug:
  print('args: ', args)


print('\n\nAuto RH\n\n')
rh.login(username=args.robin_user,
         password=args.robin_pass,
         expiresIn=86400,
         by_sms=True)


if args.ticker:
  price = rh.stocks.get_latest_price(args.ticker, includeExtendedHours=True)[0]
  print('\nTicker: ', args.ticker, '\nPrice: ', price, '\n')
  quote = rh.stocks.get_quotes(args.ticker)[0]
  if args.verbose:
    print()
    pprint(quote)
    print()


if args.buy_single_limit or args.buy_single_market:
  if not args.ticker or not args.shares:
    raise Exception('please specify --args.ticker and --args.shares for single buy')

  if args.order_shares:
    rh.orders.order_buy_fractional_by_quantity( args.ticker.upper(),
                                                args.shares,
                                                timeInForce='gtc',
                                                extendedHours=args.extended_hours )
  elif args.order_cash:
    if not args.price:
      raise Exception('must specify --price for order cash mode')

    rh.orders.order_buy_fractional_by_price( args.ticker.upper(),
                                             args.shares * args.price,
                                             timeInForce='gtc',
                                             extendedHours=args.extended_hours )

  elif args.buy_single_market:
    rh.orders.order_buy_market( args.ticker.upper(),
                                args.shares )

  elif args.buy_single_limit:
    rh.orders.order_buy_limit( stock[0].upper(),
                               stock[1],
                               stock[2],
                               timeInForce='gtc',
                               extendedHours=args.extended_hours )


if args.buy_file_limit or args.buy_file_market:
  for stock in get_stocks(args.buy_file):
    if args.order_shares:
      rh.orders.order_buy_fractional_by_quantity( stock[0].upper(),
                                                  stock[1],
                                                  timeInForce='gtc',
                                                  extendedHours=args.extended_hours )
    elif args.order_cash:
      rh.orders.order_buy_fractional_by_price( stock[0].upper(),
                                               stock[1] * stock[2],
                                               timeInForce='gtc',
                                               extendedHours=False)

    elif args.buy_file_market:
      rh.orders.order_buy_market( stock[0].upper(),
                                  stock[1] )

    elif args.buy_file_limit:
      rh.orders.order_buy_limit( stock[0].upper(),
                                 stock[1],
                                 stock[2],
                                 timeInForce='gtc',
                                 extendedHours=False )


if args.crypto:
  rh.orders.order_buy_crypto_by_price('ETH',
                                      1000,
                                      timeInForce='gtc')

  rh.orders.order_buy_crypto_by_quantity('ETH',
                                         15.9,
                                         timeInForce='gtc')


  rh.orders.order_buy_crypto_limit('BTC',
                                   0.5,
                                   5000,
                                   timeInForce='gtc')


if args.query:
  print('\n\nQuery Mode\n\n')

  if not args.query_string:
    raise Exception('please specify --query-string in query mode')

  q = rh.stocks.find_instrument_data(args.query_string)
  p = PrettyTable([ 'simple_name',
                    'symbol',
                    'day_trade_ratio',
                    'margin_initial_ratio' ])

  if args.debug:
    print('\nq: ', q)
    print('\np: ', p)

  for r in q:
    x = []
    if args.debug:
      print('\nr: ', r)

    for k, v in r.items():
      if k == 'day_trade_ratio': x.append(v)
      elif k == 'margin_initial_ratio': x.append(v)
      elif k == 'simple_name': x.append(v)
      elif k == 'symbol': x.append(v)

    p.add_row(x)

  print('\n\n', p, '\n\n')


if args.earnings:
  print('\nEarnings:')
  if not args.ticker:
    raise Exception('please specify --ticker for earnings mode')

  q = rh.stocks.get_earnings(args.ticker)
  p = PrettyTable(['symbol', 'year', 'quarter', 'actual', 'estimate'])
  if args.debug:
    print('\nq: ', q, '\n')

  for s in q:
    r = []
    for k, v in s.items():
      if k == 'symbol': r.append(v)
      elif k == 'year': r.append(v)
      elif k == 'quarter': r.append(v)
      elif k == 'eps':
        if args.debug:
          print('k: ', k)
          print('v: ', v)
        for k2, v2 in v.items():
          if k2 == 'actual': r.append(v2)
          if k2 == 'estimate': r.append(v2)
    p.add_row(r)

  if args.debug:
    pprint(q)

  print('\n', p, '\n')


if args.events:
  print('\nEvents:\n')
  if not args.ticker:
    raise Exceptions('please specify --ticker in events mode')
  r = rh.stocks.get_events(args.ticker)
  pprint(r)


if args.fundamentals:
  print('\nFundamentals:\n')
  if not args.ticker:
    raise Exceptions('please specify --ticker in fundamentals mode')
  r = rh.stocks.get_fundamentals(args.ticker)
  pprint(r)


if args.news:
  print('\nNews:\n')
  if not args.ticker:
    raise Exceptions('please specify --ticker in news mode')
  r = rh.stocks.get_news(args.ticker)
  pprint(r)


if args.ratings:
  print('\nRatings:\n')
  if not args.ticker:
    raise Exceptions('please specify --ticker in ratings mode')
  r = rh.stocks.get_news(args.ticker)
  pprint(r)


if args.portfolio:
  print('\nPortfolio:\n')
  r = rh.account.build_holdings(with_dividends=False)
  if args.debug:
    pprint(r)
  p = PrettyTable([ 'stock',
                    'price',
                    'quantity',
                    'avg buy',
                    'equity',
                    '% change',
                    '$ change',
                    'PE ratio',
                    '% portfolio', ])

  total = 0
  for k, v in r.items():
    q = []
    q.append(k)
    for k2, v2 in v.items():
      if k2 == 'price': q.append(round(float(v2), 2))
      elif k2 == 'quantity': q.append(round(float(v2), 2))
      elif k2 == 'average_buy_price': q.append(round(float(v2), 2))
      elif k2 == 'equity': q.append(round(float(v2), 2))
      elif k2 == 'percent_change': q.append(round(float(v2), 2))
      elif k2 == 'equity_change':
        q.append(round(float(v2), 2))
        total = total + float(v2)
      elif k2 == 'pe_ratio': q.append(v2)
      elif k2 == 'percentage': q.append(round(float(v2), 2))
    p.add_row(q)
  print('\n', p, '\n')
  print('total: ', round(total, 2))
  print()


if args.positions:
  q = rh.account.get_open_stock_positions()
  p = PrettyTable([ 'symbol', 'avg cost', 'quantity' ])

  if args.debug:
    pprint(q)

  total = 0
  for item in q:
    r = []
    for k, v in item.items():
      if k == 'symbol': r.append(v)
      elif k == 'average_buy_price':
        r.append(round(float(v), 2))
        total = total + float(v)
      elif k == 'quantity': r.append(round(float(v), 2))
      if args.debug:
        print(r)
    p.add_row(r)

  print('\n', p, '\n')
  print('total cost: ', round(total, 2))
  print()


if args.dividends:
  q = rh.account.get_total_dividends()
  print('\ntotal dividends: ', round(q, 2), '\n')


if args.logout:
  rh.logout()
