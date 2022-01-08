__author__ = "Ethan Posner"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0,1dev"
__maintainer__ = "Ethan Posner"
__status__ = "Production"

import datetime as dt
import os
from typing import Dict
import pickle

import pandas as pd
import yfinance as yf


class DataRetrievalInfo:
    """
    Keeps track of data which was previously retrieved.

    This will allow for data which was previously stored to be retrieved in the specified state

    For example, if stock data already exists which covers the year 2020, and data for may of 2020 is retrieved, this data should be reused
    instead of querying an API for it again.
    """

    def __init__(self, time, start, end, interval):
        """
        :param time: date string (YYYY-MM-DD) or datetime indicating when the data was retrieved
        :param start: date string (YYYY-MM-DD) or datetime indicating the start of the retrieved data
        :param end: date string (YYYY-MM-DD) or datetime indicating the end of the retrieved data
        :param interval: Indicates the resolution of the data instances retrieved.
            Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        """
        self.time = dt.datetime.strptime(time, "%Y-%d-%m") if isinstance(time, str) else time
        self.start = dt.datetime.strptime(start, "%Y-%d-%m") if isinstance(start, str) else start
        self.end = dt.datetime.strptime(end, "%Y-%d-%m") if isinstance(end, str) else end
        self.interval = interval


class StockDataProvider:

    def __init__(self, ticker_directory=os.path.join('stored_data', 'tickers')):
        """

        :param tolerance: Expiration value for ticker data in seconds. e.g. if stock is more than 300 seconds old, get
        new data.
        :param ticker_directory: Location to store pickled stock data in
        """

        self.ticker_directory = ticker_directory

        # information about the last time a specific ticker was retrieved
        # format: "ticker_str": DataRetrievalInfo
        self.last_retrieval_info_dict: Dict[str, DataRetrievalInfo] = {}

        # time delta values for valid intervals. Allows for data to be updated effectively.
        self.interval_deltas = {
            "1m":  dt.timedelta(minutes=1),
            "2m":  dt.timedelta(minutes=2),
            "5m":  dt.timedelta(minutes=5),
            "15m": dt.timedelta(minutes=15),
            "30m": dt.timedelta(minutes=30),
            "60m": dt.timedelta(minutes=60),
            "90m": dt.timedelta(minutes=90),
            "1h":  dt.timedelta(hours=1),
            "1d":  dt.timedelta(days=1),
            "5d":  dt.timedelta(days=5),
            "1wk": dt.timedelta(weeks=1),
            "1mo": dt.timedelta(days=30),
            "3mo": dt.timedelta(days=90)
        }

        self.MAX_PAST = "1970-01-01"

    def store_ticker(self, ticker_symbol: str, **kwargs) -> pd.DataFrame:
        r"""
        Query yahoo finance for any new stock data and store it as a csv file in self.ticker_directory

        :param \**kwargs: See below

        : Keyword Arguments:
            * *start* (``str``) --
              Start time for data. Can be string (YYYY-MM-DD) or datetime
            * *end* (``str``) --
              End time for data. Can be string (YYYY-MM-DD) or datetime
            * *interval* (``str``) --
              How much space should be between each data item; the data resolution
        """

        ticker_symbol = ticker_symbol.upper()

        start = kwargs['start'] if 'start' in kwargs else self.MAX_PAST
        end = kwargs['end'] if 'end' in kwargs else dt.datetime.now()
        interval = kwargs['interval'] if 'interval' in kwargs else '1d'

        # create a new directory to store the data if it doesn't already exist
        if not os.path.exists(self.ticker_directory):
            os.mkdirs(self.ticker_directory)

        # get stock data from yahoo finance
        ticker_dataframe = yf.download(ticker_symbol, start=start, end=end, interval=interval)

        self.last_retrieval_info_dict[ticker_symbol] = DataRetrievalInfo(dt.datetime.now(), start=start, end=end, interval=interval)
        ticker_dataframe.to_csv(os.path.join(self.ticker_directory, f'{ticker_symbol}.csv'))

        # pickle the DataRetrievalInfo object
        with open(os.path.join(self.ticker_directory, f"{ticker_symbol}.dri.pkl"), 'wb') as f:
            pickle.dump(self.last_retrieval_info_dict[ticker_symbol], f)

        return ticker_dataframe

    def get_ticker(self, ticker_symbol: str, **kwargs) -> pd.DataFrame:
        r"""
        See if the current stock data is up to date. If it is, then return it. If not, call self.store_ticker() to query yahoo finance for
        up-to-date stock data.
        This process allows for less API calls to be made which has the following benifits:
        - Results in a shorter runtime
        - Reduces chance of being banned from accessing yahoo finance

        :param ticker_symbol: A stock ticker to get data for e.g. 'MSFT'
        :param \**kwargs: See below
        :return: Pandas dataframe containing data for the given ticker

        : Keyword Arguments:
            * *start* (``str``) --
              Start time for data. Can be string (YYYY-MM-DD) or datetime
            * *end* (``str``) --
              End time for data. Can be string (YYYY-MM-DD) or datetime
            * *interval* (``str``) --
              How much space should be between each data item; the data resolution
        """

        ticker_dataframe = None

        ticker_symbol = ticker_symbol.upper()

        start = kwargs['start'] if 'start' in kwargs else self.MAX_PAST
        end = kwargs['end'] if 'end' in kwargs else dt.datetime.now()
        interval = kwargs['interval'] if 'interval' in kwargs else '1d'

        tolerance = self.interval_deltas[interval]

        ticker_file_path = os.path.join(self.ticker_directory, f'{ticker_symbol}.csv')

        # if the ticker has already been stored, see if it is up to date. If not, store it again.
        if os.path.isfile(ticker_file_path):
            retrieval_info = None
            # attempt to get information about when this data was last stored
            if ticker_symbol in self.last_retrieval_info_dict:
                retrieval_info = self.last_retrieval_time_dict[ticker_symbol]
            elif os.path.isfile(os.path.join(self.ticker_directory, f"{ticker_symbol}.dri.pkl")):
                with open(os.path.join(self.ticker_directory, f"{ticker_symbol}.dri.pkl"), 'rb') as f:
                    retrieval_info = pickle.load(f)
            # if data about the last retrieval is available, see if it is too old or not the right resolution
            if retrieval_info and retrieval_info.interval == interval:
                # see if the previous data covers the right range. If not, get new data
                min_start = dt.datetime.strptime(start, "%Y-%d-%m")+tolerance if isinstance(start, str) else start+tolerance
                max_end = dt.datetime.strptime(end, "%Y-%d-%m") - tolerance if isinstance(end, str) else end+tolerance
                if retrieval_info.start <= min_start and retrieval_info.end >= max_end:
                    ticker_dataframe = pd.read_csv(ticker_file_path).loc[start:end]
            else:
                ticker_dataframe = self.store_ticker(ticker_symbol, start=start, end=end)
                print('stock data updated to latest version')
        # if the above check for valid existing ticker data was unsuccessful, retrieve new data
        if not ticker_dataframe:
            ticker_dataframe = self.store_ticker(ticker_symbol, start=start, end=end)

        return ticker_dataframe


class SimulatedStockDataProvider(StockDataProvider):

    def __init__(self, ticker_directory=os.path.join('stored_data', 'tickers'), **kwargs):
        super().__init__(self, ticker_directory)
        self.current_ticker_data = kwargs['data'] if 'data' in kwargs else None

    def get_updated_data(self, ticker, interval='1d'):
        self.current_ticker_data = super().get_ticker(ticker, interval=interval)
