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


def show_fig_in_window(figure, width=800, height=800):
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


ticker_data_dir = os.path.join('stored_data', 'tickers')
pd.options.plotting.backend = "plotly"

# store ticker values for AMD, Disney, and Tesla
tickers = ('AMD', 'DIS', 'TSLA')

ticker_symbol = 'MSFT'

# update the data if it is more than one day old
data_provider = download_data.StockDataProvider(tolerance=60*60*24)

ticker_data = ticker.Ticker(ticker_symbol)

# get all close data for Microsoft
ticker_close_data: pd.Series = ticker_data.Close
ticker_close_data.name = f'{ticker_symbol} Close Data'

avg_slope_line1: pd.Series = ticker_data.moving_avg_line(
                                                        start='03-01-2015',
                                                        end='03-01-2020'
                                                        )

avg_slope_line2: pd.Series = ticker_data.moving_avg_line(
                                                        start='03-01-2020',
                                                        end=datetime.datetime.now()
                                                        )

fig = px.line(
        x=avg_slope_line2.index,
        y=avg_slope_line2.to_list()
      )

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

# show_fig_in_window(fig)
