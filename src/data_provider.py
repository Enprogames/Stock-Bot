__author__ = "Ethan Posner"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0,1dev"
__maintainer__ = "Ethan Posner"
__status__ = "Production"

import datetime
import os
from typing import Dict

import pandas as pd
import yfinance as yf


class StockDataProvider:

    def __init__(self, tolerance=60*60*24, ticker_directory=os.path.join('stored_data', 'tickers')):
        """

        :param tolerance: Expiration value for ticker data in seconds. e.g. if stock is more than 300 seconds old, get
        new data.
        :param ticker_directory: Location to store pickled stock data in
        """

        self.ticker_directory = ticker_directory

        self.tolerance = tolerance

        self.last_retrieval_time_dict: Dict[str, datetime.datetime] = {}

    def store_ticker(self, ticker_symbol: str) -> None:

        # create a new directory to store the data if it doesn't already exist
        if not os.path.exists('stored_data'):
            os.mkdir('stored_data')
        if not os.path.exists(self.ticker_directory):
            os.mkdir(self.ticker_directory)

        ticker_file_path = os.path.join(self.ticker_directory, f'{ticker_symbol.upper()}.pkl')

        # get stock data from yahoo finance
        ticker_data = yf.Ticker(ticker_symbol)
        self.last_retrieval_time_dict[ticker_symbol] = datetime.datetime.now()

        ticker_dataframe = ticker_data.history(period='max', frequency='1d')
        ticker_dataframe.to_pickle(ticker_file_path)

    def get_ticker(self, ticker_symbol: str) -> pd.DataFrame:
        """

        :param ticker_symbol: A stock ticker to get data for e.g. 'MSFT'
        :return: Pandas dataframe containing data for the given ticker
        """

        ticker_file_path = os.path.join(self.ticker_directory, f'{ticker_symbol.upper()}.pkl')

        # if the ticker has already been stored, see if it is up to date. If not, store it again.
        if os.path.isfile(ticker_file_path):
            ticker_dataframe = pd.read_pickle(ticker_file_path)
            adjusted_time = datetime.datetime.now() - datetime.timedelta(seconds=self.tolerance)
            if ticker_symbol in self.last_retrieval_time_dict and \
                    self.last_retrieval_time_dict[ticker_symbol] < adjusted_time:
                print('stock data updated to latest version')
                self.store_ticker(ticker_symbol)
        else:
            self.store_ticker(ticker_symbol)
            ticker_dataframe = pd.read_pickle(ticker_file_path)

        return ticker_dataframe
