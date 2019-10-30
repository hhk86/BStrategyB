import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
if __name__ == "__main__":
    # df = pd.read_csv("E:/BTCdata/bitstampUSD_1-min_data_2012-01-01_to_2019-08-12.csv")
    # df["datetime"] = df["Timestamp"].apply(lambda n: dt.datetime.fromtimestamp(n))
    # df["date"] = df["datetime"].apply(lambda z: z.date())
    # df["time"] = df["datetime"].apply(lambda z: z.time())
    # df = df[["date", "time", "Close", "Volume_(BTC)", "Volume_(Currency)", "Weighted_Price"]]
    # df.to_csv("E:/BTCdata/data_from_2012.csv", index=None)
    # print(df.columns)
    # print(df)
    # df = pd.read_csv("E:/BTCdata/data_from_2012.csv")
    # df = df[df["date"] > "2017"]
    # pd.set_option("display.max_columns", None)
    # df.index = list(range(df.shape[0]))
    # print(df.shape[0])
    # df = df[df["Close"].apply(lambda x: False if pd.isna(x) else True)]
    # print(df)
    # df.to_csv("E:/BTCdata/data.csv", index=None)

    # df = pd.read_csv("E:/BTCdata/data.csv")
    # df.columns = ['date', 'time', 'price', 'Volume_(BTC)', 'Volume_(Currency)', 'Weighted_Price']
    # df.to_csv("E:/BTCdata/data.csv", index=None)




    # df = pd.read_csv("E:/BTCdata/data_from_2012.csv")
    # df = df[df["date"] > "2017"]
    # pd.set_option("display.max_columns", None)
    # df.index = list(range(df.shape[0]))
    # print(df.shape[0])
    # j = 0
    # for i in range(df.shape[0]):
    #     if not df.iloc[i, 2] > 0:
    #         df.iloc[i, 2:] = df.iloc[i - 1, 2:]
    #         j += 1
    #     if i % 1000 == 0:
    #         print('\r' + str(i) + "  " + str(j), end="  ")
    #         j = 0
    # print(df)
    # df.to_csv("E:/BTCdata/data.csv", index=None)

    # df = pd.read_csv("E:/BTCdata/data.csv")
    # df = df[df["date"] <= "2019-08-11"]
    # df.columns = ['date', 'time', 'price', 'Volume_(BTC)', 'Volume_(Currency)', 'Weighted_Price']
    # df.to_csv("E:/BTCdata/data.csv", index=False)

    df = pd.read_csv("E:/BTCdata/btc.csv")
    df_max = df.groupby(by="date")["price"].max()
    df_min = df.groupby(by="date")["price"].min()
    df_diff = df_max - df_min
    df_diff.to_csv("E:/BTCdata/range.csv")
    print(df_diff)
    # print(df_max)