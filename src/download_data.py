import datetime
import os

import pandas as pd
import yfinance as yf


def store_ticker(ticker_symbol: str):

    ticker_directory = os.path.join('stored_data', 'tickers')

    if not os.path.exists('stored_data'):
        os.mkdir('stored_data')
    if not os.path.exists(ticker_directory):
        os.mkdir(ticker_directory)

    ticker_file_path = os.path.join(ticker_directory, f'{ticker_symbol.upper()}.pkl')

    ticker_data = yf.Ticker(ticker_symbol)
    ticker_dataframe = ticker_data.history(period='1d', start='2020-1-1', end=datetime.datetime.now()
                                           .strftime('%Y-%m-%d'))
    ticker_dataframe.to_pickle(os.path.join(ticker_directory, f'{ticker_symbol.upper()}.pkl'))


def get_ticker(ticker_symbol: str, tolerance=300):
    """

    :param ticker_symbol: A stock ticker to get data for e.g. 'MSFT'
    :param tolerance: Expiration value for ticker data in seconds. e.g. if stock is more than 300 seconds old, get
    new data.
    :return: Pandas dataframe containing data for the given ticker
    """

    ticker_directory = os.path.join('stored_data', 'tickers')

    ticker_file_path = os.path.join(ticker_directory, f'{ticker_symbol.upper()}.pkl')

    # if the ticker has already been stored, see if it is up to date. If not, store it again.
    if os.path.isfile(ticker_file_path):
        ticker_dataframe = pd.read_pickle(ticker_file_path)
        latest_time = ticker_dataframe.index[-1]
        if latest_time < datetime.datetime.now() - datetime.timedelta(seconds=tolerance):
            print('new stock data retrieved')
            store_ticker(ticker_symbol)
    else:
        store_ticker(ticker_symbol)
        ticker_dataframe = pd.read_pickle(ticker_file_path)

    return ticker_dataframe
