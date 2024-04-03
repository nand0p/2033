from argparse import ArgumentParser
from prettytable import PrettyTable
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
parser.add_argument('--debug', action='store_true', help='debug')
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
  print('\n', accounts.list_accounts(resp_format='json'), '\n')


if args.balances:
  print('\n', accounts.get_account_balance(os.environ['ETRADE_ID'], resp_format='json'), '\n')


if args.portfolio:
  total_gain = 0
  total_value = 0
  print()
  print(accounts.get_account_portfolio(os.environ['ETRADE_ID'], resp_format='json'))
  print()
  print('Total Gain: ' + str(round(total_gain, 2)))
  print('Total Value: ' + str(round(total_value, 2)))
  print()


if args.orders:
  print('\n', accounts.list_transactions(os.environ['ETRADE_ID'], resp_format='json'), '\n')
  print('\n', orders.list_orders(accountIDKey, resp_format='json'), '\n')


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
