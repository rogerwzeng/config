'''
HarvardX Summer 2022
CSCI-101: Foundations of Data Science and Engineering
PSET #8: Stock Portforlio Analysis
Name: Roger Zeng
'''

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# Stock class to store historic data
# symbol: stock symbol, string
# daily_close: daily close value (nx2) array with date as index
# start: start date
# end: end date
class Stock:
    # class contructor
    def __init__(self, symbol, daily):
        self.symbol = symbol
        self.daily = daily

    # calculate daily rate of return, first day always zero
    def DRR(self, start, end):
        series = np.array(self.daily[start:end])
        yesterday = np.insert(series, 0, series[0])
        yesterday = np.delete(yesterday, len(yesterday)-1)
        return (series - yesterday)/yesterday


# Portforlio class
# symbols: list of stock symbols that make up the portforlio
# weights: list of relative weights of stocks, must add up to 1
class Portforlio:
    # class constructor
    def __init__(self, symbols, weights):
        self.symbols = symbols
        self.weights = weights
        self.all = zip(symbols, weights)

        try:
            assert(len(symbols) == len(weights))
            assert(sum(weights) == 1)
        except AssertionError:
            print("Error in porforlio parameter")
            return

    # portforlio daily rate of return
    def port_drr(self, start, end):
        print("Port DRR called")
        for i, j in self.all:
            print(i, j)


# portforlio decorator
def port_dec(func):
    def inner(var_a):
        print("Decorator Func")
        # iterate through list and call action func
        return [func(i) for i in var_a]
    return inner


# action function
@port_dec
def action(indat):
    return indat**2


# submission flag, set to False for dev and unit test
submission = False


def main():
    # house keeping
    if submission:
        file_dir = '/autograder/source/'
    else:
        file_dir = ''

    # import data
    df = pd.read_csv(file_dir+'all_stocks.csv', header=0,
            parse_dates=['Date'], index_col=0)
    tickers = list(df.columns)
    stocks = []

    # instantiate stock objects
    for i, j in enumerate(tickers):
        stocks.append(Stock(j, df[j]))

    # 1) compare IBM and WalMart
    start = "1-1-2019"
    end = "4-18-2022"

    ibm_drr = stocks[0].DRR(start, end)
    wmt_drr = stocks[1].DRR(start, end)
    result_1 = ttest_ind(ibm_drr, wmt_drr)

    # process t-test results
    iw_pvalue = result_1.pvalue

    if iw_pvalue < 0.05:
        iw_diff = 'Yes'
    else:
        iw_diff = 'No'

    if not submission:
        print("\nQ1: IBM v.s. WalMart")
        print(ibm_drr.mean(), wmt_drr.mean())
        print(ibm_drr.std(), wmt_drr.std())
        print(result_1.statistic, result_1.pvalue)
        print(f"iw_diff = {iw_diff}")

    # 2) IBM + WalMart portforlio
    iwp_rr = ibm_drr.mean() * 0.4 + wmt_drr.mean() * 0.6
    if not submission:
        print("\nQ2: IBM + WalMart Portforlio")
        print(f"iwp_rr = {iwp_rr}")

    # 3) MSFT + AMZN portforlio
    msft_drr = stocks[2].DRR(start, end)
    amzn_drr = stocks[3].DRR(start, end)

    map_rr = msft_drr.mean() * 0.4 + amzn_drr.mean() * 0.6
    if not submission:
        print("\nQ3: Microsoft + Amazon Portforlio")
        print(f"map_rr = {map_rr}")

    # 4) portforlio 1 and 2 comparison
    if map_rr > iwp_rr:
        best_portforlio = 2
    elif iwp_rr > map_rr:
        best_portforlio = 1
    else:
        print("Two portforlios have the same avg drr!")

    if not submission:
        print("\nQ4: Which Portforlio is better?")
        print(f"Best Portforlio = {best_portforlio}")

    # 5) WalMart better or worse pre-pandemic
    pre_start = "1-1-2019"
    pre_end = "3-14-2020"
    dur_start = "3-15-2020"
    dur_end = "5-25-2021"

    # Avg DRR before and during Covid for Walmart
    wmt_pre = stocks[1].DRR(pre_start, pre_end).mean()
    wmt_dur = stocks[1].DRR(dur_start, dur_end).mean()

    # Better during Covid?
    if wmt_dur > wmt_pre:
        better_w_covid = 'Yes'
    elif wmt_dur < wmt_pre:
        better_w_covid = 'No'
    else:
        print("Pre and During Covid, Walmart the same!")

    if not submission:
        print("\nQ5: Walmart better during Covid?")
        print(f"Better during Covid = {better_w_covid}")


if __name__ == '__main__':
    main()
