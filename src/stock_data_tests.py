#!/usr/bin/env python

__author__ = "Ethan Posner"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0,1dev"
__maintainer__ = "Ethan Posner"
__status__ = "Production"

import datetime
import os

import tkinter as tk
from PIL import ImageTk, Image

import plotly.graph_objects as go
import pandas as pd
import data_provider
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
data_provider = data_provider.StockDataProvider()
msft_data = data_provider.get_ticker(ticker_symbol, interval='1d')
print(msft_data)

exit(0)

ticker_data = ticker.Ticker(ticker_symbol, start='01-01-2020', end=datetime.datetime.now())

# get all close data for Microsoft
ticker_close_data: pd.Series = ticker_data.Close
ticker_close_data.name = f'{ticker_symbol} Close Data'

secondary_trend1: pd.Series = ticker_data.moving_avg_line(
    start='03-01-2020',
    end='09-01-2020'
)

secondary_trend2: pd.Series = ticker_data.moving_avg_line(
    start='09-01-2020',
    end='03-01-2021'
)

secondary_trend3: pd.Series = ticker_data.moving_avg_line(
    start='03-01-2021',
    end='09-01-2021'
)

primary_trend: pd.Series = ticker_data.moving_avg_line(
    start='03-01-2020',
    end=datetime.datetime.now() - datetime.timedelta(days=5)
)

fig = go.Figure()

fig.add_scatter(
    x=secondary_trend1.index,
    y=secondary_trend1.to_list(),
    name='Secondary Trend'
)

fig.add_scatter(
    x=secondary_trend2.index,
    y=secondary_trend2.to_list(),
    name='Secondary Trend'
)

fig.add_scatter(
    x=secondary_trend3.index,
    y=secondary_trend3.to_list(),
    name='Secondary Trend'
)

fig.add_scatter(
    x=primary_trend.index,
    y=primary_trend.to_list(),
    name='Primary Trend'
)


fig.add_candlestick(
    x=ticker_data.index,
    open=ticker_data['Open'],
    high=ticker_data['High'],
    low=ticker_data['Low'],
    close=ticker_data['Close']
)

date_location = ticker_close_data.loc['03-01-2020':'04-01-2020']
print(date_location)

# fig.add_vline(x=date_location[0],
#               line_color='white', line_width=1000)
# fig.add_vline(x=['11-01-2020'], line_width=3, line_dash="dash", line_color="green")

fig.add_trace(go.Bar(x=['03-01-2020', '04-01-2020'], y=[200, 250], opacity=0.5))
# fig.add_hrect(y0=0.9, y1=200, line_width=0, fillcolor="red", opacity=0.2)

fig.update_layout(title=f'{ticker_symbol} Close', yaxis_title='Close', xaxis_title='Date')

# show figure in browser window
fig.show()

ticker = ticker.Ticker(ticker_symbol)

# show_fig_in_window(fig)
