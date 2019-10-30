import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import math
import sys
import os


class Strategy():
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.all_data = pd.read_csv(ticker + ".csv")
        self.date_list = sorted(list(set(self.all_data["date"])))
        self.x = list(range(1440))
        self.xtick = list(range(0, 1441, 120))
        self.xticklabel = list(range(0, 25, 2))
        self.plot = True

    def backtest(self) -> None:
        # self.stat_df = pd.DataFrame(columns=["sig_type", "direction", "open_price", "close_price", "pnl", "date"])
        for i in range(len(self.date_list)):
            self.backtest_oneday(i)

    def backtest_oneday(self, i: int) -> None:
        date = self.date_list[i]
        self.initDailyParam(pos_type="all", date=date, i=i)
        ax = None
        fig, ax = self.initPlot()

        # for n, xpos, ypos, delta in zip(self.Nl, self.xMl, self.yMl, self.slope_list):
        #     # Check close signal when we have positions
        #     if self.long_num > 0:
        #         sig, close_type = self.checkCloseLongSignal(n, ypos, delta)
        #         if sig is True:
        #             self.closeLongPosition(ax, n, xpos, ypos, close_type)
        #     if self.short_num > 0:
        #         sig, close_type = self.checkCloseShortSignal(n, ypos, delta)
        #         if sig is True:
        #             self.closeShortPosition(ax, n, xpos, ypos, close_type)
        #
        #     if self.long_num < 1 or self.short_num < 1:
        #         # Check open signals when we do not have full position
        #         sig, sig_type, h1 = self.checkOpenSignal(n)
        #         if sig == 'B' and self.long_num < 1:
        #             self.long_sig_type = sig_type
        #             self.long_num += 1
        #             self.long_start_pos = n
        #             self.long_start_price = ypos
        #             self.long_peak_pos = n
        #             self.long_peak_price = ypos
        #             self.long_h1 = h1
        #             if self.plot is True:
        #                 self.plotSignal(ax, n, xpos, ypos, sig, sig_type)
        #         elif sig == 'S' and self.short_num < 1:
        #             self.short_num += 1
        #             self.short_sig_type = sig_type
        #             self.short_start_pos = n
        #             self.short_start_price = ypos
        #             self.short_nadir_pos = n
        #             self.short_nadir_price = ypos
        #             self.short_h1 = h1
        #             if self.plot is True:
        #                 self.plotSignal(ax, n, xpos, ypos, sig, sig_type)
        #

        ax.set_xticks(self.xtick, self.xticklabel)
        ax.set_title(date + " PNL:" + str(round(self.pnl, 3)) )
        fig.savefig("/Users/hank/Desktop/BStrategy/plot/" + self.date + ".png")
        plt.close()
        print(date)

    def initDailyParam(self, pos_type="all", date=None, i=None) -> None:
        if pos_type == "all":
            self.date = date
            df = self.all_data.iloc[1440 * i: 1440 * (i + 1)].copy()
            self.y = df["price"].tolist()
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
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.plot(self.x, self.y, color="lightgray", linewidth=1)
        ax.plot(self.x, self.y, ".", color="lightgray", markersize=3)
        for i in range(1440):
            if abs(self.slope_list[i]) > 1:
                ax.text(self.x[i], self.y[i] + 5, str(self.slope_list[i]), fontsize=5)
        plt.title(self.date, size=15)
        return fig, ax

if __name__ == "__main__":
    obj = Strategy("btc")
    obj.backtest()