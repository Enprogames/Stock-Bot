import datetime

import numpy as np
import pandas as pd
import yfinance as yf

import download_data


class Ticker(pd.DataFrame):
    """
    Represents a stock market ticker. Holds data
    """

    def __init__(self, symbol):

        # update to latest stock data if it is older than 5 minutes
        stock_data_provider = download_data.StockDataProvider(tolerance=60*60*24)

        yfinance_ticker_data = stock_data_provider.get_ticker(symbol)

        super().__init__(yfinance_ticker_data)

        self.symbol = symbol

    def update_data(self):
        """
        Update this ticker for the latest available data
        """
        pass

    def slope_at_point(self, point: int) -> float:
        """
        Find the slope of the graph at a point
        :param point: The point at which the slope will be calculated
        :return: Slope of graph at given point
        """
        graph = self.Close.to_array()

        return graph[point + 1] - graph[point]

    def moving_avg(self, start=None, end=None) -> float:

        if not start:
            start = self.index[0]
        if not end:
            end = self.index[-1]

        mask = (self.Close.index >= start) & (self.Close.index <= end)
        graph = self.Close.loc[mask]

        avg_slope_val: float
        graph_len: int = len(graph)

        # find the average slope of the graph
        avg_slope_val = sum([graph[x_val + 1] - graph[x_val] for x_val in range(0, graph_len - 1)]) / graph_len

        return avg_slope_val

    def moving_avg_line(self, start: datetime.datetime = None, end: datetime.datetime = None) -> pd.Series:

        if not start:
            start = self.index[0]
        if not end:
            end = self.index[-1]

        mask = (self.Close.index >= start) & (self.Close.index <= end)
        graph = self.Close.loc[mask]

        tan_line_vals: np.array = np.empty(len(graph))

        avg_slope_val: float
        graph_len: int = len(graph)

        # find the average slope of the graph
        avg_slope_val = sum([graph[x_val + 1] - graph[x_val] for x_val in range(0, graph_len - 1)]) / graph_len

        # find the best y-intercept so that the middle of the equation is at the average height of the graph
        avg_height: float = graph.to_numpy().sum() / graph_len

        # find what the height of this tangent line should be in the middle
        middle_height = avg_slope_val * (graph_len / 2)

        # find how high up the tangent line should start
        y_int = avg_height - middle_height

        for x_val in range(graph_len):
            # tangent line: y = mx + b
            tan_line_vals[x_val] = avg_slope_val * x_val + y_int

        return pd.Series(tan_line_vals, index=graph.keys(), name='Moving Avg')
