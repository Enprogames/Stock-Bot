import numpy as np
import pandas as pd
import yfinance as yf


class Ticker(pd.DataFrame):
    """
    Represents a stock market ticker. Holds data
    """

    def __init__(self, symbol):
        yfinance_ticker_data = yf.Ticker(symbol)

        super().__init__(yfinance_ticker_data.history(period='max'))

        self.symbol = symbol

    def moving_avg(self):
        pass

    def slope_at_point(self, graph: np.array, point: int):
        """
        Find the slope of the graph at a point
        :param graph: A numpy array containing the y axis of the graph
        :param point: The point at which the slope will be calculated
        :return: Slope of graph at given point
        """

        return graph[point + 1] - graph[point]

    def moving_avg_line(self, graph: pd.Series) -> pd.Series:
        tan_line_vals: np.array = np.empty(len(graph))

        avg_slope_val: float
        graph_len: int = len(graph)

        # find the average slope of the graph
        avg_slope_val = sum([self.slope_at_point(graph, x_val) for x_val in range(0, graph_len - 1)]) / graph_len
        print(avg_slope_val)

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
