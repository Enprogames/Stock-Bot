import datetime
from typing import List
import os
import io

import tkinter as tk
from PIL import ImageTk, Image

import plotly.express as px
import numpy as np
import pandas as pd
import download_data


def show_fig(fig, width=800, height=800):
    root = tk.Tk()
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()

    # turn figure into Image
    if not os.path.exists("images"):
        os.mkdir("images")

    fig.write_image("images/fig.jpeg", width=width, height=height)
    image_file = Image.open("images/fig.jpeg")
    image = ImageTk.PhotoImage(image_file)

    canvas.create_image(20, 20, anchor=tk.NW, image=image)
    root.mainloop()


def slope_at_point(graph: List[float], point: int):
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
        slope_total += slope_at_point(graph, x_val)

    avg_slope = slope_total/graph_len

    # find the best y-intercept so that the middle of the equation is at the average height of the graph
    avg_height: float = 0
    for point in graph:
        avg_height += point
    avg_height /= graph_len

    # find what the height of this tangent line should be in the middle
    middle_height = avg_slope*(graph_len/2)

    y_int = avg_height - middle_height

    for x_val in range(graph_len):
        # tangent line: y = mx + b
        tan_line_vals.append(avg_slope*x_val+y_int)

    return tan_line_vals


if not os.path.exists('stored_data'):
    os.mkdir('stored_data')

# store ticker values for AMD, Disney, and Tesla
tickers = ('AMD', 'DIS', 'TSLA')

ticker = 'MSFT'

if not os.path.isfile(f'stored_data/{ticker.lower()}.pkl'):
    download_data.store_ticker(ticker.lower())

# get all close data for Microsoft
ticker_close_data = pd.read_pickle(f'stored_data/{ticker.lower()}.pkl').Close

ticker_close_list = ticker_close_data.tolist()

avg_slope = avg_tan_line(ticker_close_list)

fig = px.line(ticker_close_list, title=f'{ticker}')
#plt.plot(avg_slope, label='MSFT avg slope')

show_fig(fig)
