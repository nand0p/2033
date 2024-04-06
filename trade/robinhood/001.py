from argparse import ArgumentParser
import robin_stocks.robinhood as rs
import os

parser = ArgumentParser()
parser.add_argument('--ticker', type=str, help='ticker to execute')
parser.add_argument('--positions', action='store_true', help='show positions')
parser.add_argument('--orders', action='store_true', help='show orders')
parser.add_argument('--history', action='store_true', help='show history')
parser.add_argument('--details', action='store_true', help='show stock details')
parser.add_argument('--debug', action='store_true', help='debug')
parser.add_argument('--all', action='store_true', help='store all true')
parser.add_argument('--buy-market', action='store_true', help='execute buy from file')
args = parser.parse_args()



robin_user = os.environ.get("ROBINHOOD_USER")
robin_pass = os.environ.get("ROBINHOOD_PASS")

if args.debug:
  print('__dict__: ', rs.__dict__)

r = rs.login(username=robin_user,
             password=robin_pass,
             expiresIn=86400,
             by_sms=True)


if args.positions:
  rs.account.get_all_positions()


if args.orders:
  rs.orders.get_all_open_stock_orders()


if args.history:
  data= rs.stocks.get_stock_historicals(args.ticker, interval="10minute", span="year")
  dataframe= pd.DataFrame(data)


if args.details:
  details = rs.stocks.get_fundamentals([args.ticker], info=None)
  print('stock details: ', details)


if args.ticker:
  price = rs.stocks.get_latest_price(args.ticker, includeExtendedHours=True)
  price = float(price[0])


if args.buy_market:
  rs.orders.order_buy_fractional_by_quantity(args.ticker, 10)
