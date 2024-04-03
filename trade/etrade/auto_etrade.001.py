from argparse import ArgumentParser
from prettytable import PrettyTable
from rauth import OAuth1Service
from pprint import pprint
import webbrowser
import xmltodict
import requests
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

order_headers = {'accountIdKey': os.environ['ETRADE_ID'],
                 'PlaceOrderRequest': { 'orderType': 'EQ',
                                        'clientOrderId': secrets.token_hex(20),
                                        'previewIds': [ previews ],
                                        'order': 


if args.debug:
  print('text code: ', text_code)
  print('session: ', session)


if args.ticker:
  url = 'https://api.etrade.com/v1/market/quote/' + args.ticker
  response = session.get(url)
  if response is None or response.status_code != 200:
    raise Exception('url broken: ' + url + '\n--> response: ' + r.text)

  q = xmltodict.parse(response.text)
  if args.debug:
    print()
    print('api: ', url)
    print('response text: ', response.text)
    print('ticker: ', args.ticker)
    print()

  quote = q['QuoteResponse']['QuoteData']
  print()
  pprint(quote)
  print()

  ticker_table = PrettyTable([ 'last',
                               'bid',
                               'ask',
                               'change',
                               'change%' ])

  ticker_table.add_row([ quote['All']['lastTrade'],
                         quote['All']['bid'],
                         quote['All']['ask'],
                         quote['All']['changeClose'],
                         quote['All']['changeClosePercentage'] ])

         #<companyName>ALPHABET INC CAP STK CL C</companyName>
         #<dividend>0.0</dividend>
         #<eps>23.5639</eps>
         #<high>1186.2856</high>
         #<high52>1186.89</high52>
         #<low>1171.76</low>
         #<low52>894.79</low52>
         #<open>1175.31</open>
         #<previousClose>1168.06</previousClose>
         #<previousDayVolume>1620909</previousDayVolume>
         #<totalVolume>1167544</totalVolume>
         #<marketCap>410276824480.00</marketCap>
         #<sharesOutstanding>348952000</sharesOutstanding>
         #<declaredDividend>0.0</declaredDividend>
         #<pe>49.57</pe>
         #<week52LowDate>1499110344</week52LowDate>
         #<week52HiDate>1517257944</week52HiDate>
         #<averageVolume>1451490</averageVolume>

  print()
  print(ticker_table)
  print()




if args.account_summary:
  url = args.api + '/v1/accounts/list.json'
  response = session.get(url, header_auth=True)

  if args.debug:
    print('account url: ', url)
    print('headers: ', response.request.headers)
    print('response: ', response.text)

  if response is not None and response.status_code == 200:
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


if args.buy_file_market:
  with open(args.buy_file, 'r') as file:
  data = json.load(file)

  for x in data:
    for stock, value in x.items():
      shares = value[0]
      print('BUY:', stock, ' \tshares:', shares)
      order = MarketOrder('BUY', shares)
      contract = Stock(stock)
      if not args.confirm:
        print()
        print('====> DRY-RUN <====')
        print()

      else:
        print(https://api.etrade.com/v1/accounts/{accountIdKey}/orders/place)


if args.buy_file_limit:
  with open(args.buy_file, 'r') as file:
    data = json.load(file)

  for x in data:
    for stock, value in x.items():
      shares = value[0]
      price = value[1]
      print('BUY:', stock, ' \tshares:', shares, '\tprice:', price)
      order = LimitOrder('BUY', shares, price)
      contract = Stock(stock)

      if not args.confirm:
        print()
        print('====> DRY-RUN <====')
        print()

      else:
        print(https://api.etrade.com/v1/accounts/{accountIdKey}/orders/place)
