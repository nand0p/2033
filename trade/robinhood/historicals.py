import robin_stocks.robinhood as rh
from argparse import ArgumentParser
from pprint import pprint
import os


parser = ArgumentParser()
parser.add_argument('--stock', type=str, default='AAPL', help='stock')
parser.add_argument('--debug', action='store_true', help='debug mode')
parser.add_argument('--robin-user',
                    type=str,
                    default=os.environ.get('ROBINHOOD_USER'),
                    help='robinhood username')
parser.add_argument('--robin-pass',
                    type=str,
                    default=os.environ.get('ROBINHOOD_PASS'),
                    help='robinhood password')
args = parser.parse_args()


if args.debug:
  print('args: ', args)


print('\n\nAuto RH\n\n')
rh.login(username=args.robin_user,
         password=args.robin_pass,
         expiresIn=86400,
         by_sms=True)


history = rh.stocks.get_stock_historicals(args.stock)
pprint(history)
