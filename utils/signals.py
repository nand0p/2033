import matplotlib.pyplot as plt



def OBV(df):
    df["obv"] = np.where(df['Close'] > df['Close'].shift(1), df['Volume'], 
                         np.where(df['Close'] < df['Close'].shift(1), -df['Volume'], 0)).cumsum()
    xdate = [x.date() for x in df.index]
    plt.figure(figsize=(15, 10))
    
    # plot the original closing line
    plt.subplot(211)
    plt.plot(xdate, df.Close, label="close")
    plt.xlim(xdate[0], xdate[-1])
    plt.legend()
    plt.grid()
    
    # plot volume and OBV
    plt.subplot(212)
    plt.title("OBV")
    # plt.bar(xdate, df.Volume, label="volume")
    plt.plot(xdate, df.obv, label="obv")
    plt.xlim(xdate[0], xdate[-1])
    plt.legend()
    plt.grid(True)



def plot_RSI(df, window):
    diff = df.Close.diff(periods=1).values
    xdate = [x.date() for x in df.index]
    RSI = []
    for i in range(window+1, len(xdate)):
        neg = 0
        pos = 0
        for value in diff[i-window:i+1]:
            if value > 0:
                pos += value # accumulate positive diff
            if value < 0:
                neg += value # accumulate negative diff
        pos_ave = pos/window # average price of positive diff
        neg_ave = np.abs(neg/window) # average absolute price of negative diff
        rsi = pos_ave/(pos_ave+neg_ave)*100
        RSI.append(rsi)

    # draw RSI figure
    plt.plot(xdate[window+1:], RSI, label = "RSI {}".format(window), lw=2.5, alpha=0.6)
    plt.xlim(xdate[window+1], xdate[-1])
    plt.ylim(0,100)
    plt.legend()



def RSI(df, windows):
    xdate = [x.date() for x in df.index]
    plt.figure(figsize=(15, 10))
    
    # plot the original closing line
    plt.subplot(211)
    plt.plot(xdate, df.Close, label="close")
    plt.xlim(xdate[0], xdate[-1])
    plt.legend()
    plt.grid()
    
    # plot RSI
    plt.subplot(212)
    plt.grid()
    plt.title("RSI")
    for window in windows:
        plot_RSI(df, window)

    # fill area above 70 and below 30
    plt.fill_between(xdate, np.ones(len(xdate))*30, color="blue", alpha=0.1)
    plt.fill_between(xdate, np.ones(len(xdate))*70, np.ones(len(xdate))*100, color="red", alpha=0.1)
    
    # draw dotted lines at 70 and 30
    plt.plot(xdate, np.ones(len(xdate))*30, color="blue", linestyle="dotted")
    plt.plot(xdate, np.ones(len(xdate))*70, color="red", linestyle="dotted")
    plt.show()



def MACD(df, s, l, signal):
    df["macd"] = df.Close.ewm(span=s, min_periods=1).mean() - df.Close.ewm(span=l, min_periods=1).mean()
    df["signal"] = df.macd.ewm(span=signal, min_periods=1).mean()
    df["diff"] = df["macd"] - df["signal"]

    xdate = [x.date() for x in df.index]
    plt.figure(figsize=(15, 10))
    
    # plot the original closing line
    plt.subplot(211)
    plt.plot(xdate, df.Close, label="close")
    plt.xlim(xdate[0], xdate[-1])
    plt.legend()
    plt.grid()
    
    # plot MACD and signal
    plt.subplot(212)
    plt.title("MACD")
    plt.plot(xdate, df.macd, label="macd")
    plt.plot(xdate, df.signal, label="signal")
    plt.xlim(xdate[0], xdate[-1])
    plt.legend()
    plt.grid(True)

    # Cross points
    for i in range(1, len(df)):
        if df.iloc[i-1]["diff"] < 0 and df.iloc[i]["diff"] > 0:
            print("{}:GOLDEN CROSS".format(xdate[0]))
            plt.scatter(xdate[i], df.iloc[i]["macd"], marker="o", s=100, color="b", alpha=0.9)

        if df.iloc[i-1]["diff"] > 0 and df.iloc[i]["diff"] < 0:
            print("{}:DEAD CROSS".format(xdate[0]))
            plt.scatter(xdate[i], df.iloc[i]["macd"], marker="o", s=100, color="r", alpha=0.9)




def SMA(df, s, l):
    df["sma"] = df.Close.rolling(window=s).mean()
    df["lma"] = df.Close.rolling(window=l).mean()
    df["diff"] = df.sma - df.lma

    xdate = [x.date() for x in df.index]
    plt.figure(figsize=(15, 5))
    plt.plot(xdate, df.Close, label="close")
    plt.plot(xdate, df.sma,label="short")
    plt.plot(xdate, df.lma,label="long")
    plt.xlim(xdate[0], xdate[-1])
    plt.grid()

    # Cross points
    for i in range(1, len(df)):
        if df.iloc[i-1]["diff"] < 0 and df.iloc[i]["diff"] > 0:
            print("{}:GOLDEN CROSS".format(xdate[i]))
            plt.scatter(xdate[i], df.iloc[i]["sma"], marker="o", s=100, color="b", alpha=0.9)

        if df.iloc[i-1]["diff"] > 0 and df.iloc[i]["diff"] < 0:
            print("{}:DEAD CROSS".format(xdate[i]))
            plt.scatter(xdate[i], df.iloc[i]["sma"], marker="o", s=100, color="r", alpha=0.9)

    plt.legend()
