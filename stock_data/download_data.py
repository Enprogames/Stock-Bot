import datetime

import yfinance as yf


def store_ticker(ticker: str):
    ticker_data = yf.Ticker(ticker)
    ticker_dataframe = ticker_data.history(period='1d', start='2020-1-1', end=datetime.datetime.now()
                                               .strftime('%Y-%m-%d'))

    ticker_dataframe.to_pickle(f'stored_data/{ticker.lower()}.pkl')
