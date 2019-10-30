import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import math
import sys
import os
import random
from multiprocessing import Process, Queue

def backtest_slice(ticker):
    obj = Strategy(ticker)
    obj.backtest()



class Strategy():
    def __init__(self, ticker) -> None:
        if 'slice' not in ticker:
            self.ticker = ticker
            self.all_data = pd.read_csv("E:/BTCdata/" + ticker + ".csv")
        else:
            self.all_data = pd.read_csv(ticker)
        self.date_list = sorted(list(set(self.all_data["date"])))
        self.all_data["quantity"] = self.all_data["Volume_(BTC)"].apply(lambda x: round(x, 2))
        self.x = list(range(1440))
        self.xtick = list(range(0, 1441, 120))
        self.xticklabel = list(range(0, 25, 2))
        self.plot = True

    def multi_backtest(self, arg_dict=None, plot=False):

        if not os.path.exists("E:\\data_slice\\" + self.ticker + "\\data_slice_9.csv"):
            self.slice()
        q = Queue()
        jobs = list()
        for i in range(0, 10):
            ticker = "E:\\data_slice\\" + self.ticker + "\\data_slice_" + str(i) + ".csv"
            p = Process(target=backtest_slice, args=(ticker,))
            jobs.append(p)
            p.start()
            print("Start process" + str(i))
        # for i in range(0, 10):
        #     df = df.append(q.get())
        for job in jobs:
            job.join()


    def slice(self, process_num=10):
        n = process_num
        N = len(self.date_list)
        try:
            os.removedirs("E:\\data_slice\\" + self.ticker)
            print("Re-writing the data slice of", self.ticker)
        except:
            print("Writing new data slice of", self.ticker)
        os.makedirs("E:\\data_slice\\" + self.ticker)
        for i in range(0, n):
            date_scope = self.date_list[math.floor(i * (N / n)): math.floor((i + 1) * (N / n))]
            data_slice = self.all_data[self.all_data["date"].apply(lambda s: True if s in date_scope else False)]
            data_slice.to_csv("E:\\data_slice\\" + self.ticker + "\\data_slice_" + str(i) + ".csv", index=False)
        print("Slice data into " + str(n) + " part.\n Save data slice to: " + "E:\\data_slice\\" + self.ticker)

    def backtest(self) -> None:
        # self.stat_df = pd.DataFrame(columns=["sig_type", "direction", "open_price", "close_price", "pnl", "date"])
        for i in range(len(self.date_list)):
            self.backtest_oneday(i)

    def backtest_oneday(self, i: int) -> None:
        date = self.date_list[i]
        self.initDailyParam(pos_type="all", date=date, i=i)
        ax = None
        fig, ax = self.initPlot()


        for n in range(1440):
            sig_type = self.RAP_Signal(n)
            self.test_plot_signal(ax, n, sig_type)

        ax.set_xticks(self.xtick, self.xticklabel)
        ax.set_title(date + " PNL:" + str(round(self.pnl, 3)) )
        fig.savefig("backtest/" + self.date + ".png")
        plt.close()
        print(date)

    def initDailyParam(self, pos_type="all", date=None, i=None) -> None:
        if pos_type == "all":
            self.date = date
            df = self.all_data.iloc[1440 * i: 1440 * (i + 1)].copy()
            self.y = df["price"].tolist()
            self.q = df["quantity"]. tolist()
            raw_slope_list = [0,] + list(np.diff(self.y))
            self.slope_list = [int(round(t / self.y[0] * 1000)) for t in raw_slope_list]
            self.y_min = df["price"].min()
            self.y_max = df["price"].max()
            self.y_mid = 0.5 * (self.y_min + self.y_max)
            self.pnl = 0
        if pos_type == "long" or pos_type == "all":
            self.long_num = 0
            self.long_sig_type = None
            self.long_start_pos = None
            self.long_start_price = None
            self.long_peak_pos = None
            self.long_peak_price = None
            self.long_h1 = 0
            self.long_reach_6 = False
        if pos_type == "short" or pos_type == "all":
            self.short_num = 0
            self.short_sig_type = None
            self.short_start_pos = None
            self.short_start_price = None
            self.short_nadir_pos = None
            self.short_nadir_price = None
            self.short_h1 = 0
            self.short_reach_6 = False


    def initPlot(self) -> (plt, plt):
        y_offset = self.y[0] / 1000 * 0.5
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(self.x, self.y, color="lightgray", linewidth=1)
        ax.plot(self.x, self.y, ".", color="lightgray", markersize=2)
        for i in range(1440):
            slope =  self.slope_list[i]
            if slope > 0:
                color = "red"
            elif slope < 0:
                color = "green"
            else:
                color = "blue"
            # ax.plot([self.x[i],], [self.y[i], ], marker=".", color=color, markersize=1)
            if self.date == "2017-01-16":
                ax.text(self.x[i] - 1, self.y[i] + y_offset, str(abs(slope)), fontsize=10, color=color)
            elif abs(slope) > 1:
                ax.text(self.x[i] - 1, self.y[i] + y_offset, str(abs(slope)), fontsize=10, color=color)
            # ax.plot([self.x[i], self.x[i] + 0.001], [self.y_mid, self.y_mid + self.q[i] / self.y[0] * 50] , color=color)
        plt.title(self.date, size=15)
        return fig, ax


    def count(self, n: int, threshold: int, *args):
        k = 0
        for h in args:
            if h >= threshold:
                k += 1
        if k >= n:
            return True
        else:
            return False

    def RAP_Signal(self, n: int):
        if n < 8:
            return None
        h8, h7, h6, h5, h4, h3, h2, h1 = self.slope_list[n - 7 : n + 1]
        if self.count(2, 3, h1, h2):
            return "RAPB1"
        if self.count(2, 3, h1, h2, h3) and min([h1, h2, h3]) >= 0 and h1 + h2 + h3 >= 7:
            return "RAPB2"
        # if self.count(3, 2, h1, h2, h3, h4) and min([h1, h2, h3, h4]) >= -1 and h1 + h2 + h3 + h4 >= 8:
        #     return "RAPB3"
        # if self.count(2, 2, h1, h2, h3, h4) and min([h1, h2, h3, h4]) >= 0 and h1 + h2 + h3 + h4 >= 8:
        #     return "RAPB3"

        if self.count(2, 2, h1, h2, h3, h4, h5) and self.count(4, 1, h1, h2 ,h3 ,h4, h5)\
                and min([h1, h2, h3, h4, h5]) >= 0 and h1 + h2 + h3 + h4 + h5 >= 5:
            return "RAPB3"

        if self.count(1, 2, h1, h2, h3, h4, h5, h6, h7, h8) and self.count(4, 1, h1, h2, h3, h4, h5, h6, h7, h8)\
            and self.count(7, 0, h1, h2, h3, h4, h5, h6, h7, h8) and h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 >= 6:
            return "RAPB4"

    def test_plot_signal(self, ax, n, sig_type):
        if sig_type is None:
            return
        elif sig_type == "RAPB1":
            diff = 2
        elif sig_type == "RAPB2":
            diff = 3
        elif sig_type == "RAPB3":
            diff = 4
        elif sig_type == "RAPB4":
            diff = 8
        ax.plot(self.x[n - diff: n + 1], self.y[n - diff: n + 1], color="gold")
        ax.plot([self.x[n],], [self.y[n],], marker='*', color="red")
        ax.text(self.x[n], self.y[n]-20, sig_type[-1])






if __name__ == "__main__":
    obj = Strategy("btc")
    obj.multi_backtest()