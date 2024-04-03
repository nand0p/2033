from argparse import ArgumentParser
from prettytable import PrettyTable
from rauth import OAuth1Service
import webbrowser
import requests
import json
import os


parser = ArgumentParser()
parser.add_argument('--pause', type=int, default=1, help='sleep iteration')
parser.add_argument('--api', type=str, default='https://api.etrade.com', help='etrade api')
parser.add_argument('--ticker', type=str, help='ticker to execute')
parser.add_argument('--institution', type=str, default='BROKERAGE', help='institution type')
parser.add_argument('--shares', type=int, help='shares')
parser.add_argument('--price', type=float, help='price')
parser.add_argument('--account-summary', action='store_true', help='show account summary')
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

etrade = OAuth1Service(name='etrade',
                       consumer_key=os.environ['ETRADE_KEY'],
                       consumer_secret=os.environ['ETRADE_SECRET'],
                       request_token_url=args.api + '/oauth/request_token',
                       access_token_url=args.api + '/oauth/access_token',
                       authorize_url='https://us.etrade.com/e/t/etws/authorize?key={}&token={}',
                       base_url=args.api)

request_token, request_token_secret = etrade.get_request_token(
  params={'oauth_callback': 'oob', 'format': 'json'})

authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
webbrowser.open(authorize_url)
text_code = input('Please accept agreement and enter verification code from browser: ')
session = etrade.get_auth_session(request_token,
                                  request_token_secret,
                                  params={'oauth_verifier': text_code})


if args.ticker:
  #market = Market(session, base_url)
  #market.quotes()
  print('ticket: ', args.ticker)


if args.account_summary:
  url = args.api + '/v1/accounts/list.json'
  response = session.get(url, header_auth=True)

  if args.debug:
    print('account url: ', url)
    print('headers: ', response.request.headers)
    print('response: ', response.text)

  if response.status_code == 200:
    accounts = response.json()["AccountListResponse"]["Accounts"]["Account"]

    p = PrettyTable([ 'AccountId',
                      'AccountIdKey',
                      'AccountMode',
                      'AccountDesc',
                      'AccountName',
                      'AccountType',
                      'InstitutionType',
                      'AccountStatus' ])

    for account in accounts:
      p.add_row([ account['accountId'],
                  account['accountIdKey'],
                  account['accountMode'],
                  account['accountDesc'],
                  account['accountName'],
                  account['accountType'],
                  account['institutionType'],
                  account['accountStatus'] ])

  print()
  print('account summary: ' + url)
  print()
  print(p)
  print()


if args.balances:
  r = PrettyTable(['balance', 'description', 'value', 'margin power', 'cash power'])
  url = args.api + '/v1/accounts/' + os.environ['ETRADE_ID'] + '/balance.json'
  params = {'instType': args.institution, 'realTimeNAV': 'true'}
  headers = {'consumerkey': os.environ['ETRADE_KEY']}
  response = session.get(url, header_auth=True, params=params, headers=headers)

  if args.debug:
    print('balances url: ', url)
    print('params: ', params)
    print('send headers: ', headers)
    print('return headers: ', response.request.headers)
    print('response: ', response.text)

  if response is not None and response.status_code == 200:
    balance_data = response.json()['BalanceResponse']
    r.add_row([ balance_data['accountId'],
                balance_data['accountDescription'],
                round(balance_data['Computed']['RealTimeValues']['totalAccountValue'], 2),
                round(balance_data['Computed']['marginBuyingPower'], 2),
                round(balance_data['Computed']['cashBuyingPower'], 2) ])

  print()
  print('balances: ' + url)
  print()
  print(r)
  print()


if args.portfolio:
  q = PrettyTable(['Stock', 'Quantity', 'LastPrice', 'PricePaid', 'TotalGain', 'MarketValue'])
  url = args.api + '/v1/accounts/' + os.environ['ETRADE_ID'] + '/portfolio.json'
  response = session.get(url, header_auth=True)

  if args.debug:
    print('portfolio url: ', url)
    print('headers: ', response.request.headers)
    print('response: ', response.text)

  total_gain = 0
  total_value = 0
  if response is not None and response.status_code == 200:
    for acctPortfolio in response.json()["PortfolioResponse"]["AccountPortfolio"]:
      for position in acctPortfolio["Position"]:
        q.add_row([ position['symbolDescription'],
                    position['quantity'],
                    round(position['Quick']['lastTrade'], 2),
                    round(position['pricePaid'], 2),
                    round(position['totalGain'], 2),
                    round(position['marketValue'], 2) ])
        total_gain = total_gain + position['totalGain']
        total_value = total_value + position['marketValue']

  print()
  print('portfolio: ' + url)
  print()
  print(q)
  print()
  print('Total Gain: ' + str(round(total_gain, 2)))
  print('Total Value: ' + str(round(total_value, 2)))
  print()
