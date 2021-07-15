import datetime
from typing import List
import os

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import download_data


def slope(graph: List[float], point: int):
    """
    Find the slope of the graph at a point
    :param graph: A numpy array containing the y axis of the graph
    :param point: The point at which the slope will be calculated
    :return: Slope of graph at given point
    """

    return graph[point+1] - graph[point]


def avg_tan_line(graph: List[float]) -> List[float]:

    tan_line_vals: List[float] = []

    avg_slope: float
    graph_len: int = len(graph)
    slope_total: float = 0

    for x_val in range(0, graph_len-1):
        slope_total += slope(graph, x_val)

    avg_slope = slope_total/graph_len

    for x_val in range(graph_len):
        # tangent line: y = mx + b
        print(x_val)
        tan_line_vals.append(avg_slope*x_val+graph[0])

    return tan_line_vals

if not os.path.exists('stored_data'):
    os.mkdir('stored_data')

if not os.path.isfile('stored_data/msft.pkl'):
    download_data.store_ticker('MSFT')

# store ticker values for AMD, Disney, and Tesla
tickers = ('AMD', 'DIS', 'TSLA')

# get all close data for Microsoft
msft_close_data = pd.read_pickle('stored_data/msft.pkl').Close

msft_close_list = msft_close_data.tolist()

avg_slope = avg_tan_line(msft_close_list)

# get close prices for tickers
#stock_prices = yf.download(tickers, start="2020-1-1", end=datetime.datetime.now().strftime('%Y-%m-%d'), peroid='ytd').Close

#print(stock_prices)
#print(ticker_data.history(period='1d', start='2020-1-1', end=datetime.datetime.now().strftime('%Y-%m-%d')))


# stock_prices['AMD'].plot()
# stock_prices['DIS'].plot()
# stock_prices['TSLA'].plot()
#msft_close_data.plot(label='MSFT')
plt.plot(msft_close_list, label='MSFT')
plt.plot(avg_slope, label='MSFT avg slope')

plt.title('Stock Prices for AMD, Disney, and Tesla')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
