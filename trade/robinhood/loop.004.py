while True:
    price = rs.stocks.get_latest_price('AAPL', includeExtendedHours=True)
    price = float(price[0]) # convert to single float

    if price > 400:
        rs.orders.cancel_stock_order(stoploss_order_id)
        rs.orders.order_sell_market('AAPL', 10)
        print("STOP LOSS CANCELLED AND MARKET SELL TRIGGERED, APPLE PRICE:", price)
        print("ORDER TRIGGERED at {}".format(pd.Timestamp.now()))
        break
    
    print("STILL WAITING, APPLE PRICE:", price)
    sleep(15)
