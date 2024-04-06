import os

robin_user = os.environ.get("robinhood_username")
robin_pass = os.environ.get("robinhood_password")

rs.login(username=robin_user,
         password=robin_pass,
         expiresIn=86400,
         by_sms=True)

rs.orders.order_buy_fractional_by_price(symbol,
                                       ammountInDollars,
                                       timeInForce='gtc',
                                       extendedHours=False)

rs.orders.order_buy_fractional_by_price('AAPL',
                                        500,
                                        timeInForce='gtc',
                                        extendedHours=False)


rs.orders.order_buy_fractional_by_quantity(symbol,
                                          quantity,
                                          timeInForce='gtc',
                                          extendedHours=False)

rs.orders.order_buy_fractional_by_quantity('AAPL',
                                          7.3,
                                          timeInForce='gtc',
                                          extendedHours=False)



rs.orders.order_buy_limit(symbol,
                          quantity,
                          limitPrice,
                          timeInForce='gtc',
                          extendedHours=False)

rs.orders.order_buy_limit('AAPL,
                          5,
                          450,
                          timeInForce='gtc',
                          extendedHours=False)

rs.orders.order_buy_crypto_by_price('ETH', 
                                 1000,
                                 timeInForce='gtc')

rs.orders.order_buy_crypto_by_quantity('ETH', 
                                 15.9,
                                 timeInForce='gtc')


rs.orders.order_buy_crypto_limit('BTC', 
                                 0.5,
                                 5000,
                                 timeInForce='gtc')


price = rs.stocks.get_latest_price('MA', includeExtendedHours=True
# assigning price to first (and only) item of list and converting from str to float
mastercard_price = float(price[0])

rs.logout()
