from argparse import ArgumentParser
from pprint import pprint
from ib_insync import *
import requests
import json


ib = IB()

parser = ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=4001, help='ib proxy port')
parser.add_argument('-z', '--host', type=str, default='localhost', help='ib proxy hostname')
parser.add_argument('-t', '--ticker', type=str, default='AAPL', help='ticker to execute')
parser.add_argument('-as', '--account-summary', action='store_true', help='show account summary')
parser.add_argument('-av', '--account-values', action='store_true', help='show account values')
parser.add_argument('-o', '--open', action='store_true', help='show open orders')
parser.add_argument('-c', '--closed', action='store_true', help='show closed orders')
parser.add_argument('-d', '--debug', action='store_true', help='debug')
parser.add_argument('-pl', '--pnl', action='store_true', help='profit and loss')
parser.add_argument('-bm', '--buy-market', type=float, default=0.0001)
parser.add_argument('-pos', '--positions', action='store_true', help='list positions')
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

if args.confirm:
  print('stock: ', args.ticker)
  print('conId: ', conId)
  print('buy_market: ', args.buy_market)
  order = MarketOrder('BUY', args.buy_market)
  trade = ib.placeOrder(contract, order)
  print('Wait for Trade')
  while not trade.isDone():
    print(ib.waitOnUpdate())
  print('Trade Log')
  trade.log

if args.positions:
  print('Portfolio')
  portfolio = ib.portfolio()
  pprint(portfolio)
  print('Positions')
  positions = ib.positions()
  pprint(positions)


print('\n..::Exiting Session::..\n')
ib.disconnect()
