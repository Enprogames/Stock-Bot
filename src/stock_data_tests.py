import datetime
import time
from typing import List
import os

import tkinter as tk
from PIL import ImageTk, Image

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import download_data
import ticker


def show_fig(figure, width=800, height=800):
    root = tk.Tk()
    root.geometry(f'+{-1500}+{50}')
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()

    # turn figure into Image
    if not os.path.exists("images"):
        os.mkdir("images")

    figure.write_image("images/fig.jpeg", width=width, height=height)
    image_file = Image.open("images/fig.jpeg")
    image = ImageTk.PhotoImage(image_file)

    canvas.create_image(0, 0, anchor=tk.NW, image=image)
    root.mainloop()


def slope_at_point(graph: np.array, point: int):
    """
    Find the slope of the graph at a point
    :param graph: A numpy array containing the y axis of the graph
    :param point: The point at which the slope will be calculated
    :return: Slope of graph at given point
    """

    return graph[point+1] - graph[point]


def moving_avg_line(graph: pd.Series) -> pd.Series:

    tan_line_vals: np.array = np.empty(len(graph))

    avg_slope_val: float
    graph_len: int = len(graph)

    # find the average slope of the graph
    avg_slope_val = sum([slope_at_point(graph, x_val) for x_val in range(0, graph_len-1)]) / graph_len
    print(avg_slope_val)

    # find the best y-intercept so that the middle of the equation is at the average height of the graph
    avg_height: float = graph.to_numpy().sum() / graph_len

    # find what the height of this tangent line should be in the middle
    middle_height = avg_slope_val*(graph_len/2)

    # find how high up the tangent line should start
    y_int = avg_height - middle_height

    for x_val in range(graph_len):
        # tangent line: y = mx + b
        tan_line_vals[x_val] = avg_slope_val*x_val+y_int

    return pd.Series(tan_line_vals, index=graph.keys(), name=f'Moving Avg')


ticker_data_dir = os.path.join('stored_data', 'tickers')
pd.options.plotting.backend = "plotly"

# store ticker values for AMD, Disney, and Tesla
tickers = ('AMD', 'DIS', 'TSLA')

ticker_symbol = 'MSFT'

# update the data if it is more than one day old
data_provider = download_data.StockDataProvider(tolerance=60*60*24)

ticker_data = data_provider.get_ticker(ticker_symbol)

# get all close data for Microsoft
ticker_close_data: pd.Series = ticker_data.Close
ticker_close_data.name = f'{ticker_symbol} Close Data'

avg_slope_line: pd.Series = moving_avg_line(ticker_close_data)

fig = px.line(
        x=avg_slope_line.index,
        y=avg_slope_line.to_list()
      )

candlestick_graph = go.Figure(data=[go.Candlestick(
                                   x=ticker_data.index,
                                   open=ticker_data['Open'],
                                   high=ticker_data['High'],
                                   low=ticker_data['Low'],
                                   close=ticker_data['Close']
                                  )])

fig.add_candlestick(
                                   x=ticker_data.index,
                                   open=ticker_data['Open'],
                                   high=ticker_data['High'],
                                   low=ticker_data['Low'],
                                   close=ticker_data['Close']
                                  )

fig.update_layout(title=f'{ticker_symbol} Close', template='plotly_dark', yaxis_title='Close', xaxis_title='Date')

# show figure in browser window
fig.show()

ticker = ticker.Ticker(ticker_symbol)

# show_fig(fig)
