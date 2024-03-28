from argparse import ArgumentParser
from pprint import pprint
from ib_insync import *
from prettytable import PrettyTable
import requests
import json
import time


ib = IB()

parser = ArgumentParser()
parser.add_argument('--port', type=int, default=4001, help='ib proxy port')
parser.add_argument('--pause', type=int, default=1, help='sleep iteration')
parser.add_argument('--host', type=str, default='localhost', help='ib proxy hostname')
parser.add_argument('--ticker', type=str, default='AAPL', help='ticker to execute')
parser.add_argument('--account-summary', action='store_true', help='show account summary')
parser.add_argument('--account-values', action='store_true', help='show account values')
parser.add_argument('--open', action='store_true', help='show open orders')
parser.add_argument('--closed', action='store_true', help='show closed orders')
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('--pnl', action='store_true', help='profit and loss')
parser.add_argument('--buy-market', action='store_true', help='execute buy as market')
parser.add_argument('--buy-limit', action='store_true', help='execute buy as limit')
parser.add_argument('--buy', action='store_true', help='execute buy from file')
parser.add_argument('--positions', action='store_true', help='list positions')
parser.add_argument('--portfolio', action='store_true', help='list portfolio')
parser.add_argument('--confirm', action='store_true', help='flag required to execute trade')
args = parser.parse_args()


print('Connect')
conn = ib.connect(host=args.host, port=args.port, clientId=1, timeout=5)
pprint(conn)

print('Stock: ', args.ticker)
stock = Stock(symbol=args.ticker,
              exchange='SMART',
              primaryExchange='SMART',
              currency='USD')

stock_obj = ib.qualifyContracts(stock)
conId = stock_obj[0].conId

if args.debug:
  pprint(conId)
  pprint(stock)
  pprint(stock_obj)

contract = Contract(conId=conId,
                    secType='STK',
                    symbol=args.ticker,
                    currency='USD',
                    exchange='SMART',
                    primaryExchange='SMART')

print('Current Time')
current_time = ib.reqCurrentTime()
pprint(current_time.isoformat())
print('Account: ')
managed_accounts = ib.managedAccounts()
pprint(managed_accounts)


if args.account_values:
  print()
  print('Account Values')
  print()
  account_values = ib.accountValues()
  for v in account_values:
    if args.debug:
      pprint(v)
    print(v[0], v[1], v[2], v[3])

if args.account_summary:
  print()
  print('Account Summary')
  print()
  account_summary = ib.accountSummary()
  for v in account_summary:
    if args.debug:
      pprint(v)
    print(v[0], v[1], v[2], v[3])

if args.open:
  print('Open Trades')
  open_trades = ib.openTrades()
  pprint(open_trades)
  print('Orders')
  orders = ib.orders()
  pprint(orders)
  print('Open Orders')
  open_orders = ib.openOrders()
  pprint(open_orders)

if args.closed:
  print('Trades')
  trades = ib.trades()
  pprint(trades)
  print('Fills')
  fills = ib.fills()
  pprint(fills)
  print('Exections')
  executions = ib.executions()
  pprint(executions)

if args.pnl:
  print('PnL')
  pnl = ib.pnl()
  pprint(pnl)
  print('PnL Single')
  pnl_single = ib.pnlSingle()
  pprint(pnl_single)


if args.buy:
  if not args.confirm:
    print()
    print('====> DRY-RUN <====')
    print()

  with open('buy.json', 'r') as file:
    data = json.load(file)

  for x in data:
    for stock, value in x.items():
      shares = value[0]
      price = value[1]
      print('BUY:', stock, ' \tshares:', shares, '\tprice:', price)

      if args.buy_limit:
        order = LimitOrder('BUY', shares, price)
      elif args.buy_market:
        order = MarketOrder('BUY', shares)
      else:
        raise Exception('must select either --buy-limit or --buy-market')

      contract = Stock(stock)
      if args.debug:
        print('------>', order)
        print('------>', contract)

      if args.confirm:
        time.sleep(args.pause)

        try:
          orderId = ib.placeOrder(contract, order)
        except IbEx as e:
          print('ERROR: ', e.errCode, e.errMsg)
        else:
          print('SUCCESS: ', orderId)

        print('Wait for Trade')
        while not orderId.isDone():
          print(ib.waitOnUpdate())
        print('Trade Log')
        print(orderId.log)

  if not args.confirm:
    print()
    print('====> DRY-RUN <====')
    print()


if args.portfolio:
  total = 0
  profit = 0
  portfolio = ib.portfolio()
  if portfolio:
    print("Current Portfolio:")
    p = PrettyTable(['stock', 'shares', 'cost', 'value', 'price', 'pnl', 'unpnl'])
    for position in portfolio:
      if args.debug:
        print('stock:', position.contact.symbol,
              'shares: ', position.position,
              'avgCost: ', round(position.avgCost, 2),
              'marketValue: ', round(position.marketValue, 2),
              'marketPrice: ', round(position.marketPrice, 2),
              'realizedPNL: ', position.realizedPNL,
              'unrealizedPNL: ', position.unrealizedPNL)
      p.add_row([position.contract.symbol,
                 position.position,
                 round(position.averageCost, 2),
                 round(position.marketValue, 2),
                 round(position.marketPrice, 2),
                 position.realizedPNL,
                 position.unrealizedPNL])
      total = total + position.marketValue
      profit = profit + position.unrealizedPNL

  print(p)
  print()
  print('total profit: ', round(profit, 2))
  print('total value: ', round(total, 2))
  print()


if args.positions:
  positions = ib.positions()
  if positions:
    print("Current Positions:")
    p = PrettyTable(['stock', 'shares', 'cost'])
    for position in positions:
      if args.debug:
        print('stock:', position.contract.symbol,
              'shares: ', position.position,
              'avgCost: ', round(position.avgCost, 2))
      p.add_row([position.contract.symbol,
                 position.position,
                 round(position.avgCost, 2)])

  print(p)


ib.disconnect()
