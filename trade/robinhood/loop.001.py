while True:
    try:
        price = rs.stocks.get_latest_price('MA', includeExtendedHours=True)
        # assigning price to first (and only) item of list and converting from str to float
        mastercard_price = float(price[0])

        if mastercard_price < 280:
            try:
                rs.orders.order_buy_fractional_by_price('V', 500)
                break

            except Exception as e:
                print("Error placing order:", e)
        else:
            sleep(15)

    except Exception as e:
        print("Error fetching latest price:", e)

print("ORDER TRIGGERED at {}".format(pd.Timestamp.now()))
