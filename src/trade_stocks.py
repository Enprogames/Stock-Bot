from abc import ABC, abstractmethod
from typing import Tuple


class StockTraderADT(ABC):

    def __init__(self, trade_api: str, credentials: Tuple):
        """

        :param credentials: Required credentials for trading using the API. Some APIs may require a single key while
        others may provide multiple. See the docstring for the desired API for more info.
        """
        pass

    def buy(self, symbol: str, amount: float) -> bool:
        """

        :param symbol: Ticker symbol of stock to buy
        :param amount: How many stocks to buy
        :return: Whether or not the trade was a success
        """
        pass

    def sell(self, symbol: str, amount: float) -> bool:
        """

        :param symbol: Ticker symbol of stock to sell
        :param amount: How many stocks to sell
        :return: Whether or not the trade was a success
        """
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
            self.api_key = credentials[0]
            self.secret_key = credentials[1]

        super().__init__(trade_api, credentials)

    def buy(self, symbol: str, amount: float) -> bool:

        # buy stocks using alpaca
        if self.trade_api == 'alpaca':
            return True

    def sell(self, symbol: str, amount: str) -> bool:

        # sell stocks which were bought using alpaca
        if self.trade_api == 'alpaca':
            return True
