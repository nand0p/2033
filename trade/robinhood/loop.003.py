from time import sleep
import pandas as pd

df = pd.DataFrame(columns=['date', 'price'])

while True:
    try:
        price = rs.stocks.get_latest_price('TSLA', includeExtendedHours=True)
        # assigning price to first (and only) item of list and converting from str to float
        tesla_price = float(price[0])
        
        df.loc[len(df)] = [pd.Timestamp.now(), tesla_price]

        
        start_time = df.date.iloc[-1] - pd.Timedelta(minutes=60)
        df = df.loc[df.date >= start_time] # cuts dataframe to only include last hour of data
        max_price = df.price.max()
        min_price = df.price.min()
        
        if (df.price.iloc[-1] < max_price * 0.99 or df.price.iloc[-1] > min_price * 1.01):
            try:
                # finds current best bid for option contract we want to buy
                best_bid = rs.options.find_options_by_expiration_and_strike('TSLA',
                                                                 '2020-07-17',
                                                                 1580,
                                                                 optionType='call',
                                                                 info='bid_price')
                # converts output to float
                best_bid = float(best_bid[0])
                # we place our limit bid 0.1% above the current best bid
                our_bid = 1.001 * best_bid
                
                rs.orders.order_buy_option_limit('open', 
                                 'debit', 
                                 our_bid, 
                                 'TSLA',
                                 1,
                                 '2020-07-17', 
                                 1580, 
                                 optionType='call', 
                                 timeInForce='gtc')
                print("MOVED MORE THAN 1%, TESLA CURRENT PRICE: {} MIN PRICE: {} MAX PRICE: {}\n".format(df.price.iloc[-1], min_price, max_price))
                break
                
            except Exception as e:
                print("Error placing order:", e)
        
        else:
            print("NO ORDER, TESLA CURRENT PRICE: {} MIN PRICE: {} MAX PRICE: {}\n".format(df.price.iloc[-1], min_price, max_price))
            sleep(15)
                
    except Exception as e:
        print("Error fetching latest price:", e)
        
print("ORDER TRIGGERED at {}".format(pd.Timestamp.now()))
print("LIMIT BUY FOR OPTION CALL PLACED AT:", our_bid)
