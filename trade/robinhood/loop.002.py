# firing a pair trade when Dropbox and box diverge more than 3% over the previous day FULL EXAMPLE

dropbox_data = rs.stocks.get_stock_historicals("DBX", interval="day", span="week")
dropbox_historical = pd.DataFrame(dropbox_data)

box_data = rs.stocks.get_stock_historicals("BOX", interval="day", span="week")
box_historical = pd.DataFrame(box_data)

price_diff_yesterday = dropbox_historical.iloc[-1]['close_price'] - box_historical.iloc[-1]['close_price']

while True:
    try:
        dropbox_today = float(rs.stocks.get_latest_price('DBX', includeExtendedHours=True)[0])
        box_today = float(rs.stocks.get_latest_price('BOX', includeExtendedHours=True)[0])
        print("box today:", box_today)
        print("dropbox today:", dropbox_today)

        price_diff_today = dropbox_today - box_today

        if price_diff_today > 1.03 * price_diff_yesterday:
            try:
                # LONG BOX SHORT DROPBOX
                rs.orders.order_buy_fractional_by_price('BOX',
                                           500,
                                           timeInForce='gtc',
                                           extendedHours=False) 

                rs.orders.order_sell_fractional_by_price('DBX',            
                                           500,
                                           timeInForce='gtc',
                                           extendedHours=False) 

                print("Diverged MORE THAN 3%, YESTERDAY'S DIFFERENCE: {} TODAY'S DIFFERENCE: {} PERCENTAGE CHANGE: {}%\n".format(price_diff_yesterday, price_diff_today, (price_diff_today/price_diff_yesterday - 1)*100))
                break
            except Exception as e:
                print("Error placing orders:", e)
                sleep(15)


        else:
            print("STILL WAITING, YESTERDAY'S DIFFERENCE: {} TODAY'S DIFFERENCE: {} PERCENTAGE CHANGE: {}%\n".format(price_diff_yesterday, price_diff_today, ((price_diff_today/price_diff_yesterday - 1))*100))
            sleep(15)
    except Exception as e:
        print("Error fetching latest prices:", e)
        sleep(15)

print("ORDER TRIGGERED at {}".format(pd.Timestamp.now()))
