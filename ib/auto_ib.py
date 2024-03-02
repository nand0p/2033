from argparse import ArgumentParser
from pprint import pprint
from ib_insync import *


ib = IB()

parser = ArgumentParser()
parser.add_argument('--port', type=int, default=4001)
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--client', type=int, default=1)
parser.add_argument('--ticker', type=str, default='AAPL')
parser.add_argument('--account-summary', action='store_true')
parser.add_argument('--account-values', action='store_true')
parser.add_argument('--open', action='store_true')
parser.add_argument('--closed', action='store_true')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--pnl', action='store_true')
parser.add_argument('--buy-shares', type=float, default=0.0)
parser.add_argument('--positions', action='store_true')
parser.add_argument('--trade', action='store_true')
args = parser.parse_args()


print('connect')
conn = ib.connect(host=args.host,
                  port=args.port,
                  clientId=args.client,
                  timeout=5)
pprint(conn)

print('stock: ', args.ticker)
stock = Stock(symbol=args.ticker,
              exchange='SMART',
              currency='USD',
              primaryExchange='SMART')

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

print('current time')
current_time = ib.reqCurrentTime()
pprint(current_time.isoformat())

print('account: ')
managed_accounts = ib.managedAccounts()
pprint(managed_accounts)

if args.account_values:
  print()
  print('account values')
  print()
  account_values = ib.accountValues()
  pprint(account_values)

if args.account_summary:
  print()
  print('account summary')
  print()
  account_summary = ib.accountSummary()
  pprint(account_summary)

if args.open:
  print('open trades')
  open_trades = ib.openTrades()
  pprint(open_trades)
  print('orders')
  orders = ib.orders()
  pprint(orders)
  print('open orders')
  open_orders = ib.openOrders()
  pprint(open_orders)

if args.closed:
  print('trades')
  trades = ib.trades()
  pprint(trades)
  print('fills')
  fills = ib.fills()
  pprint(fills)
  print('exections')
  executions = ib.executions()
  pprint(executions)

if args.pnl:
  print('pnl')
  pnl = ib.pnl()
  pprint(pnl)
  print('pnl single')
  pnl_single = ib.pnlSingle()
  pprint(pnl_single)

if args.trade:
  print('stock: ', args.ticker)
  print('conId: ', conId)
  print('buy_shares: ', args.buy_shares)
  order = MarketOrder('BUY', args.buy_shares)
  trade = ib.placeOrder(contract, order)
  print('wait for trade')
  while not trade.isDone():
    print(ib.waitOnUpdate())
  print('trade log')
  trade.log

if args.positions:
  print('portfolio')
  portfolio = ib.portfolio()
  pprint(portfolio)
  print('positions')
  positions = ib.positions()
  pprint(positions)

print('exiting session')
ib.disconnect()
