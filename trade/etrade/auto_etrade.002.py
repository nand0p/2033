from time import strftime, localtime
from prettytable import PrettyTable
from argparse import ArgumentParser
from rauth import OAuth1Service
from pprint import pprint
import pyetrade
import secrets
import json
import os



parser = ArgumentParser()
parser.add_argument('--pause', type=int, default=1, help='sleep iteration')
parser.add_argument('--api', type=str, default='https://api.etrade.com', help='etrade api')
parser.add_argument('--ticker', type=str, help='ticker to execute')
parser.add_argument('--buy-file', type=str, default='../buy.json', help='file to execute')
parser.add_argument('--institution', type=str, default='BROKERAGE', help='institution type')
parser.add_argument('--shares', type=int, help='shares')
parser.add_argument('--price', type=float, help='price')
parser.add_argument('--account-summary', action='store_true', help='show account summary')
parser.add_argument('--orders', action='store_true', help='show orders')
parser.add_argument('--balances', action='store_true', help='show account balances')
parser.add_argument('--portfolio', action='store_true', help='show portfolio')
parser.add_argument('--transactions', action='store_true', help='show transactions')
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('--verbose', action='store_true', help='verbose output')
parser.add_argument('--all', action='store_true', help='store all true')
parser.add_argument('--buy-file-market', action='store_true', help='execute buy from file')
parser.add_argument('--buy-file-limit', action='store_true', help='execute buy from file')
parser.add_argument('--buy-single-market', action='store_true', help='execute market buy from ticker arg')
parser.add_argument('--buy-single-limit', action='store_true', help='execute limit buy from ticker arg')
parser.add_argument('--confirm', action='store_true', help='flag required to execute trade')
args = parser.parse_args()

if args.all:
  args.balances = True
  args.portfolio = True
  args.account_summary = True



consumer_key = os.environ['ETRADE_KEY']
consumer_secret = os.environ['ETRADE_SECRET']

oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
print('\nauthorize session: ', oauth.get_request_token(), '\n')
verifier_code = input("Enter verification code: ")
tokens = oauth.get_access_token(verifier_code)


if args.debug:
  print()
  print('tokens')
  pprint(tokens)
  print()

#authManager = pyetrade.authorization.ETradeAccessManager(
#                consumer_key,
#                consumer_secret,
#                tokens['oauth_token'],
#                tokens['oauth_token_secret'])

accounts = pyetrade.ETradeAccounts(consumer_key,
                                   consumer_secret,
                                   tokens['oauth_token'],
                                   tokens['oauth_token_secret'],
                                   dev=False)


if args.ticker:
  market = pyetrade.ETradeMarket(
    consumer_key,
    consumer_secret,
    tokens['oauth_token'],
    tokens['oauth_token_secret'],
    dev=False)

  print('\n', market.get_quote([args.ticker.upper()],resp_format='json'), '\n')


if args.account_summary:
  p = PrettyTable([ 'accountId',
                    'accountIdKey',
                    'accountMode',
                    'accountDesc',
                    'accountName',
                    'accountType',
                    'institutionType',
                    'accountStatus' ])

  r = accounts.list_accounts(resp_format='json')
  q = r['AccountListResponse']['Accounts']['Account'][0]
  if args.debug:
    print('r: ', r)
    print('q: ', q)

  p.add_row([ q['accountId'],
              q['accountIdKey'],
              q['accountMode'],
              q['accountDesc'],
              q['accountName'],
              q['accountType'],
              q['institutionType'],
              q['accountStatus'] ])

  print()
  print('account summary')
  print()
  print(p)
  print()


if args.balances:
  q = []
  if args.verbose:
    p = PrettyTable([ 'fundsForOpenOrdersCash',
                      'moneyMktBalance',
                      'cashAvailableForWithdrawal',
                      'totalAvailableForWithdrawal',
                      'netCash',
                      'cashBalance',
                      'settledCashForInvestment',
                      'unSettledCashForInvestment',
                      'fundsWithheldFromWithdrawal',
                      'marginBuyingPower',
                      'cashBuyingPower',
                      'marginBalance',
                      'accountBalance',
                      'totalAccountValue',
                      'totalLong' ])
  else:
    p = PrettyTable([ 'marginBuyingPower',
                      'cashBuyingPower',
                      'marginBalance',
                      'accountBalance',
                      'totalAccountValue',
                      'totalLong' ])

  r = accounts.get_account_balance(os.environ['ETRADE_ID'], resp_format='json')['BalanceResponse']
  if args.debug:
    print('r: ', r)

  for x, v in r.items():
    if args.debug: print('x: ', x, '\nv: ', v)
    if args.verbose:
      if x == 'Cash':
        q.append(v['fundsForOpenOrdersCash'])
        q.append(v['moneyMktBalance'])
      elif x == 'Computed':
        q.append(v['cashAvailableForWithdrawal'])
        q.append(v['totalAvailableForWithdrawal'])
        q.append(v['netCash'])
        q.append(v['cashBalance'])
        q.append(v['settledCashForInvestment'])
        q.append(v['unSettledCashForInvestment'])
        q.append(v['fundsWithheldFromWithdrawal'])
        q.append(v['marginBuyingPower'])
        q.append(v['cashBuyingPower'])
        q.append(v['marginBalance'])
        q.append(v['accountBalance'])
        q.append(v['RealTimeValues']['totalAccountValue'])
        q.append(v['RealTimeValues']['netMvLong'])
    else:
      if x == 'Computed':
        q.append(v['marginBuyingPower'])
        q.append(v['cashBuyingPower'])
        q.append(v['marginBalance'])
        q.append(v['accountBalance'])
        q.append(v['RealTimeValues']['totalAccountValue'])
        q.append(v['RealTimeValues']['netMvLong'])

  p.add_row(q)

  if args.debug:
    print('q: ', q)

  print()
  print(p)
  print()


if args.portfolio:
  total_gain = 0
  total_value = 0
  total_cost = 0

  p = PrettyTable([ 'positionId',
                    'symbolDescription',
                    'dateAcquired',
                    'pricePaid',
                    'quantity',
                    'marketValue',
                    'totalCost',
                    'totalGain',
                    'totalGainPct',
                    'pctOfPortfolio',
                    'costPerShare',
                    'lastTrade',
                    'change',
                    'changePct',
                    'volume' ])

  s = accounts.get_account_portfolio(os.environ['ETRADE_ID'], resp_format='json')
  q = s['PortfolioResponse']['AccountPortfolio'][0]['Position']
  if args.debug:
    print('q: ', q)
    print('s: ', s)

  for position in q:
    r = []
    for k, v in position.items():
      if k == 'positionId': r.append(v)
      if k == 'symbolDescription': r.append(v),
      if k == 'dateAcquired': r.append(v)
      if k == 'pricePaid': r.append(v)
      if k == 'quantity': r.append(v)
      if k == 'totalCost':
        r.append(v)
        total_cost = total_cost + v
      if k == 'marketValue':
        r.append(v)
        total_value = total_value + v
      if k == 'totalGain':
        r.append(v)
        total_gain = total_gain + v
      if k == 'totalGainPct': r.append(v)
      if k == 'pctOfPortfolio': r.append(v)
      if k == 'costPerShare': r.append(v)
      if k == 'Quick':
        r.append(v['lastTrade'])
        r.append(v['change'])
        r.append(v['changePct'])
        r.append(v['volume'])
    p.add_row(r)

  print()
  print(p)
  print()
  print('Total Cost: ' + str(round(total_cost, 2)))
  print('Total Gain: ' + str(round(total_gain, 2)))
  print('Total Value: ' + str(round(total_value, 2)))
  print()


if args.transactions:
  p = PrettyTable([ 'transactionId',
                    'transactionDate',
                    'quantity',
                    'price',
                    'symbol' ])

  r = accounts.list_transactions(os.environ['ETRADE_ID'], resp_format='json')
  s = r['TransactionListResponse']['Transaction']
  if args.debug:
    print('r: ', r)
    print('s: ', s)

  for j in s:
    q = []
    for k, v in j.items():
      if k == 'transactionId': q.append(v)
      elif k == 'transactionDate': q.append(strftime('%Y-%m-%d', localtime(v)))
      elif k == 'displaySymbol': q.append(v)
      elif k == 'brokerage':
        q.append(v.get('quantity'))
        q.append(v.get('price'))
        q.append(v.get('displaySymbol'))
    p.add_row(q)

  print()
  print(p)
  print()


if args.orders:
  orders = pyetrade.ETradeOrder(consumer_key,
                                consumer_secret,
                                tokens['oauth_token'],
                                tokens['oauth_token_secret'],
                                dev=False)

  q = orders.list_orders(accountIDKey, resp_format='json')
  if args.debug:
    print('q: ', q)


if args.buy_file_market or args.buy_file_limit:
  with open(args.buy_file, 'r') as file:
    data = json.load(file)

  for x in data:
    for stock, value in x.items():
      shares = value[0]
      print('BUY:', stock, ' \tshares:', shares, '\tprice:', price)
      if not args.confirm:
        print()
        print('====> DRY-RUN <====')
        print()

      else:
        orders = pyetrade.ETradeOrder(consumer_key,
                                      consumer_secret,
                                      tokens['oauth_token'],
                                      tokens['oauth_token_secret'],
                                      dev=True)

        if args.buy_file_limit:
          resp = order.place_option_order(resp_format = 'json',
                                          accountId = account_id,
                                          symbol = stock,
                                          limitPrice = price,
                                          quantity = shares,
                                          orderAction = 'BUY_OPEN',
                                          priceType = 'LIMIT',
                                          orderTerm = 'GOOD_FOR_DAY',
                                          allOrNone = False,
                                          clientOrderId = secrets.token_hex(20),
                                          marketSession = 'REGULAR')

        elif args.buy_file_market:
          resp = order.place_option_order(resp_format = 'json',
                                          accountId = account_id,
                                          symbol = stock,
                                          quantity = shares,
                                          orderAction = 'BUY_OPEN',
                                          priceType = 'MARKET',
                                          orderTerm = 'GOOD_FOR_DAY',
                                          allOrNone = False,
                                          clientOrderId = secrets.token_hex(20),
                                          marketSession = 'REGULAR')

        pprint(resp)
