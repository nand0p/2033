from prettytable import PrettyTable
from argparse import ArgumentParser
from pprint import pprint
from ib_insync import *
import requests
import json
import time


parser = ArgumentParser()
parser.add_argument('--port', type=int, default=4001, help='ib proxy port')
parser.add_argument('--pause', type=int, default=1, help='sleep iteration')
parser.add_argument('--host', type=str, default='localhost', help='ib proxy hostname')
parser.add_argument('--ticker', type=str, help='ticker to execute')
parser.add_argument('--shares', type=int, help='shares')
parser.add_argument('--price', type=float, help='price')
parser.add_argument('--account-summary', action='store_true', help='show account summary')
parser.add_argument('--account-values', action='store_true', help='show account values')
parser.add_argument('--open', action='store_true', help='show open orders')
parser.add_argument('--closed', action='store_true', help='show closed orders')
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('--no-wait', action='store_true', help='dont block on order execution')
parser.add_argument('--pnl', action='store_true', help='profit and loss')
parser.add_argument('--verbose', action='store_true', help='verbose')
parser.add_argument('--exchange', type=str, default='SMART', help='exchange')
parser.add_argument('--buy-file', type=str, default='../buy.json', help='file to source')
parser.add_argument('--buy-file-market', action='store_true', help='execute buy from file')
parser.add_argument('--buy-file-limit', action='store_true', help='execute buy from file')
parser.add_argument('--buy-single-market', action='store_true', help='execute market buy from ticker arg')
parser.add_argument('--buy-single-limit', action='store_true', help='execute limit buy from ticker arg')
parser.add_argument('--positions', action='store_true', help='list positions')
parser.add_argument('--portfolio', action='store_true', help='list portfolio')
parser.add_argument('--confirm', action='store_true', help='flag required to execute trade')
args = parser.parse_args()

if args.no_wait:
  wait_for_order = False
else:
  wait_for_order = True

print('Connect')
ib = IB()
conn = ib.connect(host=args.host, port=args.port, clientId=1, timeout=5)
pprint(conn)

print('Current Time')
current_time = ib.reqCurrentTime()
pprint(current_time.isoformat())

print('Account: ')
managed_accounts = ib.managedAccounts()
pprint(managed_accounts)


def wait(orderId):
  print('Wait for Trade')

  while not orderId.isDone():
    print(ib.waitOnUpdate())

  print('Trade Log')
  pprint(orderId.log)


def place_order(order, contract, pause, debug, wait_for_order):
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
      print('\nSUCCESS:\n')
      print('====> Contract: ', orderId.contract)
      print('====> Order: ', orderId.order)
      print('====> Status: ', orderId.orderStatus)
      print('====> Fills: ', orderId.fills)
      print()

    if wait_for_order:
      wait(orderId)


if args.ticker:
  print('Stock: ', args.ticker)
  stock = Stock(symbol=args.ticker,
                exchange=args.exchange,
                primaryExchange=args.exchange,
                currency='USD')

  stock_obj = ib.qualifyContracts(stock)
  conId = stock_obj[0].conId
  contract = Contract(conId=conId,
                      secType='STK',
                      symbol=args.ticker,
                      currency='USD',
                      exchange=args.exchange,
                      primaryExchange=args.exchange)

  if args.debug:
    pprint(conId)
    pprint(stock)
    pprint(stock_obj)
    pprint(contract)


if args.account_values:
  print()
  print('Account Values')
  print()
  account_values = ib.accountValues()
  t = PrettyTable(['1','2','3','4'])
  for v in account_values:
    if args.debug:
      pprint(v)
    t.add_row([v[0], v[1], v[2], v[3]])
  print(t)


if args.account_summary:
  print()
  print('Account Summary')
  print()
  account_summary = ib.accountSummary()
  t = PrettyTable(['1','2','3','4'])
  for v in account_summary:
    if args.debug:
      pprint(v)
    t.add_row([v[0], v[1], v[2], v[3]])
  print(t)


if args.open:
  orders = ib.orders()

  if args.verbose:
    print('Orders')
    pprint(orders)
    open_trades = ib.openTrades()
    print('Open Trades')
    pprint(open_trades)

  print('Open Orders')
  open_orders = ib.openOrders()
  pprint(open_orders)


if args.closed:
  if args.verbose:
    print('Trades')
    trades = ib.trades()
    pprint(trades)
    print('Exections')
    executions = ib.executions()
    pprint(executions)

  print('Fills')
  fills = ib.fills()
  pprint(fills)


if args.pnl:
  print('PnL')
  pnl = ib.pnl()
  pprint(pnl)
  print('PnL Single')
  pnl_single = ib.pnlSingle()
  pprint(pnl_single)


if args.buy_single_limit:
  if args.shares is not None and args.price is not None and args.ticker is not None:
    print('\n==> BUY LIMIT: ', args.ticker, ' \tshares:', args.shares, '\tprice:', args.price)
    order = LimitOrder('BUY', args.shares, args.price)
    contract = Stock(args.ticker, exchange=args.exchange)

    if not args.confirm:
      print('====> DRY-RUN: ', contract, '\n')

    else:
      print('====> EXEC: ', contract, '\n')
      place_order(order=order,
                  contract=contract,
                  pause=args.pause,
                  debug=args.debug,
                  wait_for_order=wait_for_order)

  else:
    raise Exception('needs: --shares --price --ticker')


if args.buy_single_market:
  if args.shares is not None and args.ticker is not None:
    print('\n==> BUY MARKET: ', args.ticker, '\tshares:', args.shares)
    order = MarketOrder('BUY', args.shares)
    contract = Stock(args.ticker)

    if not args.confirm:
      print('====> DRY-RUN: ', contract, '\n')

    else:
      print('====> EXEC: ', contract, '\n')
      place_order(order=order,
                  contract=contract,
                  pause=args.pause,
                  debug=args.debug,
                  wait_for_order=wait_for_order)

  else:
    raise Exception('needs: --shares --ticker')


if args.buy_file_limit:
    with open(args.buy_file, 'r') as file:
      data = json.load(file)

    for x in data:
      stock = x[0]
      shares = x[1]
      price = x[2]
      print('\n==> BUY: ', stock, ' \tshares:', shares, '\tprice:', price)
      order = LimitOrder('BUY', shares, price)
      s = Stock(symbol=stock,
                exchange=args.exchange,
                primaryExchange=args.exchange,
                currency='USD')

      s_obj = ib.qualifyContracts(s)
      contract = Contract(conId=s_obj[0].conId,
                          secType='STK',
                          symbol=stock,
                          currency='USD',
                          exchange=args.exchange,
                          primaryExchange=args.exchange)

      if not args.confirm:
        print('====> DRY-RUN: ', contract, '\n')

      else:
        print('====> EXEC: ', contract, '\n')
        place_order(order=order,
                    contract=contract,
                    pause=args.pause,
                    debug=args.debug,
                    wait_for_order=wait_for_order)


if args.buy_file_market:
    with open(args.buy_file, 'r') as file:
      data = json.load(file)

    if args.debug:
      print('data: ', data)

    for x in data:
      if args.debug:
        print('x: ', x)

      stock = x[0]
      shares = x[1]
      print('\n==> BUY:', stock, ' \tshares:', shares)
      order = MarketOrder('BUY', shares)
      s = Stock(symbol=stock,
                exchange=args.exchange,
                primaryExchange=args.exchange,
                currency='USD')

      s_obj = ib.qualifyContracts(s)
      contract = Contract(conId=s_obj[0].conId,
                          secType='STK',
                          symbol=stock,
                          currency='USD',
                          exchange=args.exchange,
                          primaryExchange=args.exchange)


      if not args.confirm:
        print('====> DRY-RUN: ', contract, '\n')

      else:
        print('====> EXEC: ', contract, '\n')
        place_order(order=order,
                    contract=contract,
                    pause=args.pause,
                    debug=args.debug,
                    wait_for_order=wait_for_order)


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
