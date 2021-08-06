__author__ = "Ethan Posner"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0,1dev"
__maintainer__ = "Ethan Posner"
__status__ = "Production"

from abc import ABC, abstractmethod
from typing import Tuple

import alpaca_trade_api


class StockTraderADT(ABC):

    @abstractmethod
    def __init__(self, credentials: Tuple):
        """

        :param credentials: Required credentials for trading using the API. Some APIs may require a single key while
        others may provide multiple. See the docstring for the desired API for more info.
        """
        pass

    @abstractmethod
    def buy(self, symbol: str, amount: float) -> bool:
        """

        :param symbol: Ticker symbol of stock to buy
        :param amount: How many stocks to buy
        :return: Whether or not the trade was a success
        """
        pass

    @abstractmethod
    def sell(self, symbol: str, amount: float) -> bool:
        """

        :param symbol: Ticker symbol of stock to sell
        :param amount: How many stocks to sell
        :return: Whether or not the trade was a success
        """
        pass


class AlpacaStockTrader(StockTraderADT, alpaca_trade_api.REST):

    def __init__(self, credentials: Tuple, base_url):
        alpaca_trade_api.REST.__init__(self, key_id=credentials[0], secret_key=credentials[1], base_url=base_url)

    def buy(self, symbol: str, amount: float) -> bool:
        pass

    def sell(self, symbol: str, amount: float) -> bool:
        pass


class StockTrader(StockTraderADT):

    def __init__(self, trade_api: str, credentials: Tuple):
        """

        :param trade_api: Which api to use for trading. For example, alpaca may be used to begin with, but a better
        alternative may be chosen later. In which case, another if statement would need to be put into this class for
        which one to use.
        :param credentials: The credentials to be put into the API. e.g. alpaca requires an API Key ID and a Secret Key.
        """

        self.trade_api = trade_api
        self.credentials = credentials

        if trade_api == 'alpaca':
            self.trade_api = AlpacaStockTrader(credentials, base_url="https://paper-api.alpaca.markets/")

    def buy(self, symbol: str, amount: float) -> bool:

        # buy stocks using alpaca
        if self.trade_api == 'alpaca':
            return True

    def sell(self, symbol: str, amount: str) -> bool:

        # sell stocks which were bought using alpaca
        if self.trade_api == 'alpaca':
            return True
