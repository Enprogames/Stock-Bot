__author__ = "Ethan Posner"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0,1dev"
__maintainer__ = "Ethan Posner"
__status__ = "Production"

from datetime import datetime
from abc import ABC, abstractmethod, abstractproperty
from typing import List, Dict
import traceback

import alpaca_trade_api


class StockTraderADT(ABC):

    @abstractmethod
    def __init__(self, api_params: Dict[str, any] = None):
        """

        :param api_params: Required parameters for trading if an API is used. Some APIs may require a single key while
        others may provide multiple. Some may also require base request urls or accept other parameters.
        See the docstring for the desired API trading class for more info.
        """
        pass

    @abstractmethod
    def buy(self, symbol: str, amount: float, notional: bool = False) -> bool:
        """
        Buy a specific stock in either a quantity or dollar amount. If successful, a new order object should be created.

        :param symbol: Ticker symbol of stock to buy
        :param amount: How many stocks to buy
        :param notional: Whether or not to trade with dollar amount instead of number of stocks
        :return: Whether or not the order was a success
        """
        pass

    @abstractmethod
    def sell(self, symbol: str, amount: float, notional: bool = False) -> bool:
        """
        Sell a specific stock in either a quantity or dollar amount. If successful, a new order object should be created.

        :param symbol: Ticker symbol of stock to sell
        :param amount: How many stocks to sell
        :param notional: Whether or not to trade with dollar amount instead of number of stocks
        :return: Whether or not the order was a success
        """
        pass

    @abstractmethod
    def get_symbol_orders(self, symbol: str) -> List:
        """
        Get all orders made for a specific symbol

        :param symbol: Ticker symbol of stock to get orders for (e.g. 'MSFT' for Microsoft)
        :return: orders made for the given symbol
        """
        pass

    @abstractmethod
    def get_orders(self) -> List:
        """
        Get all orders made through this trading object

        :return: List of stock order objects made through this trading object.
        """
        pass


class StockOrderADT(ABC):
    """
    An order sent for a specific stock. This differs from a position, since a stock is not owned until an order for it has gone through.

    For example, a user may buy a stock once, then see that the value has gone down and decide to buy again. Once both of these have been filled,
    they will both be added to a position object for the given stock (or a new position object will be created).
    """

    @abstractmethod
    def __init__(self, side: str, symbol: str, amount: float, notional=False, status='open', time_in_force='gtc', trade_api=None):
        """
        Create a new order object. Market orders are the only allowed type at this point. The time in force is set to 'gtc' which means
        'good till cancelled.'
        """
        pass

    @abstractproperty
    def status(self):
        """

        """
        pass

    @abstractmethod
    def cancel(self) -> bool:
        """
        This should send an API request to cancel this order. If the order has already gone through (has a status of filled), or if it is filled
        before the cancellation goes through, this method should return False, meaning the order was not cancelled.

        If the order was successfully cancelled, True should be returned.
        :return: Whether or not the cancellation was successful.
        """
        pass


class StockPositionADT(ABC):
    """
    Keeps track of how much is owned of each stock in a user's portfolio.

    These shouldn't be interacted with directly, and should only be accessed through a StockTrader object.
    """

    @abstractmethod
    def __init__(self, symbol: str, amount: float = 0):

        self.symbol = symbol
        self._amount = amount

    def add_stock(self, amount):
        """
        This should be used when more of this stock is bought
        """
        pass

    def remove_stock(self, amount):
        """
        This should be used when stock is sold and the amount owned must be reduced
        """
        pass


class UncancellableOrderException(Exception):
    """
    Should be thrown when an order cancellation is attempted but cannot be done.
    """
    pass


class StockOrder(StockOrderADT):
    """
    Allows for the storage and retrieval of data for a specific stock order. This object should be independent of any method of trading. For example,
    it should be useable for any real trading API or a simulated trading environment.
    """

    def __init__(self, side: str, symbol: str, amount: float, notional: bool = False, status: str = 'open', id: str = None, trade_api: any = None):
        self.side: str = side  # whether or not the was a 'buy' or 'sell' order
        self.symbol: str = symbol.upper()
        self.amount: int = amount
        self.notional: bool = notional
        self._status = status
        self.id: str = id
        self.trade_api: any = trade_api

        # times where certain actions occured for this trading object (e.g. when the order was created: 'created_at',
        # when the order was filled: 'filled_at')
        self.time: Dict[datetime] = {}

    @property
    def status(self, request: bool = True) -> str:
        """
        Get the current status of this order. e.g. new, filled, cancelled, etc

        :param request: Whether or not to make a new request to the trade_api for the current status. No request will be made if a trade_api was not
        specified.
        :return: The status of the order (new,partially_filled, filled, done_for_day, cancelled, expired, replaced, pending_cancel, pending_replace)
        """
        if request and self.trade_api and not self._status == 'filled':
            order_info = self.trade_api.get_order(self.id)
            if not order_info:
                order_info = self.trade_api.get_position(self.id)
            self._status = order_info.status

        return self._status

    def cancel(self):
        """
        Attempt to cancel this order. If it cannot be cancelled (e.g. it has already been filled), an UncancellableOrderException will be raised.
        """
        self.status = self.status()

        if self._status == 'filled':
            raise UncancellableOrderException("Order has already been filled")
        else:
            if self.trade_api:
                try:
                    self.trade_api.cancel()
                except alpaca_trade_api.rest.APIError:
                    traceback.print_exc()
            else:
                self._status = 'cancelled'

        return self._status

    def __str__(self):
        amount_str = f"amount: ${self.amount}" if self.notional else f"qty: {self.amount}"
        return f"{self.symbol} {self.side} order ({amount_str}, status: {self.status})"


class NotEnoughStockException(Exception):
    """
    Should be thrown when more stock is subtracted from a stock position than is currently owned.
    """
    pass


class StockPosition(StockPositionADT):

    def __init__(self, symbol: str, amount: float = 0, notional=False):
        self.symbol = symbol
        self._amount = amount

    def add_stock(self, amount):
        """
        This should be used when more of this stock is bought
        """
        self._amount += amount

    def remove_stock(self, amount):
        """
        This should be used when stock is sold and the amount owned must be reduced
        """
        self._amount -= amount

        if self.amount < 0:
            self._amount = 0
            raise NotEnoughStockException(f"Not enough of {self.symbol} was owned to sell this much! {self._amount} was owned and {amount} was \
            attempted to be subtracted")

    def __str__(self):
        return f"Position for {self.symbol} of {self._amount}"


class AlpacaStockTrader(StockTraderADT, alpaca_trade_api.REST):

    """
    Alpaca API parameter defaults:
    "APCA_API_KEY_ID": ""  # required
    "APCA_API_SECRET_KEY": ""  # required
    "APCA_API_BASE_URL": "https://api.alpaca.markets/"  # Should be added if usage of paper account is desired! This class will use the paper account
    by default anyways.
    "APCA_API_DATA_URL": "https://data.alpaca.markets"
    "APCA_RETRY_MAX": -1  # optional
    "APCA_RETRY_WAIT": -1  # optional
    "APCA_RETRY_CODES": -1  # optional
    "DATA_PROXY_WS": ""  # optional
    """

    def __init__(self, api_params: Dict[str, any]):

        # set environment variables for API
        key_id = api_params['APCA_API_KEY_ID']
        secret_key = api_params['APCA_API_SECRET_KEY']
        base_url = api_params['APCA_API_BASE_URL'] if 'APCA_API_BASE_URL' in api_params else "https://paper-api.alpaca.markets"
        # data_url = api_params['APCA_API_DATA_URL'] if 'APCA_API_DATA_URL' in api_params else "https://data.alpaca.markets"
        # retry_max = api_params['APCA_API_BASE_URL'] if 'APCA_API_BASE_URL' in api_params else -1
        # retry_wait = api_params['APCA_RETRY_WAIT'] if 'APCA_RETRY_WAIT' in api_params else -1
        # retry_codes = api_params['APCA_RETRY_CODES'] if 'APCA_RETRY_CODES' in api_params else -1
        # proxy_ws = api_params['DATA_PROXY_WS'] if 'DATA_PROXY_WS' in api_params else ""
        alpaca_trade_api.REST.__init__(self, key_id=key_id, secret_key=secret_key, base_url=base_url)

        self.orders: List[StockOrder] = []
        self.positions: Dict[str, StockPosition] = []

        # add any existing orders from the trade api
        prev_orders = self.list_orders()
        for prev_order in prev_orders:
            if prev_order.notional and int(prev_order.notional) > 0:
                self.orders.append(StockOrder(side=prev_order.side, symbol=prev_order.symbol, amount=prev_order.notional, notional=True,
                                              status=prev_order.status, trade_api=self, id=prev_order.id))
            else:
                self.orders.append(StockOrder(side=prev_order.side, symbol=prev_order.symbol, amount=prev_order.qty, notional=False,
                                              status=prev_order.status, trade_api=self, id=prev_order.id))

        prev_positions = self.list_positions()
        for prev_position in prev_positions:
            if prev_position.notional and int(prev_position.notional) > 0:
                self.positions[prev_position.symbol] = StockPosition(symbol=prev_position.symbol, amount=prev_order.notional, notional=True)
            else:
                self.positions[prev_position.symbol] = StockPosition(symbol=prev_position.symbol, amount=prev_order.qty, notional=False)

    def buy(self, symbol: str, amount: float, notional: bool = False) -> bool:

        successful = False

        symbol = symbol.upper()

        try:
            if notional:  # trade in dollar amount
                order = self.submit_order(symbol, side='buy', notional=amount, type='market')
            else:  # trade in number of stocks
                order = self.submit_order(symbol, side='buy', qty=amount)
            self.orders.append(StockOrder(side=order.side, symbol=symbol, amount=amount, notional=notional, status=order.status, id=order.id))
            successful = True
        except alpaca_trade_api.rest.APIError:
            traceback.print_exc()

        return successful

    def sell(self, symbol: str, amount: float, notional: bool = False) -> bool:

        successful = False

        symbol = symbol.upper()

        try:
            if notional:  # trade in dollar amount
                order = self.submit_order(symbol, side='sell', notional=amount, type='market')
            else:  # trade in number of stocks
                order = self.submit_order(symbol, side='sell', qty=amount)
            self.orders.append(StockOrder(side=order.side, symbol=symbol, amount=amount, notional=notional, status=order.status, id=order.id))
            successful = True
        except alpaca_trade_api.rest.APIError:
            traceback.print_exc()

        return successful

    def get_symbol_orders(self, symbol: str) -> List[str]:

        symbol = symbol.upper()

        return [order for order in self.orders if order.symbol.upper() == symbol]

    def get_orders(self) -> List[str]:
        return self.orders

    def get_position(self, symbol) -> StockPosition:
        return self.positions[symbol]

    def get_positions(self) -> List[StockPosition]:
        list(self.positions.values())


class SimulatedTrader(StockTraderADT):
    """
    Used for testing trading algorithms on historical stock data

    There are many things to keep in mind for this class to work as expected:
        - Orders shouldn't be executed immediately, and should only go through after a certain amount of time
        - The simulated trading algorithm should be executed in an environment which simulates the passage of time. For example, simulating a trading
        algorithm on 100 years of data shouldn't actually take 100 years to complete; it should be executed in a matter of minutes/seconds. For
        this to work properly, the passage of time would need to be simulated.
    """

    def __init__(self):
        pass

    def buy(self, symbol: str, amount: float, notional: bool = False) -> bool:
        symbol = symbol.upper()
        pass

    def sell(self, symbol: str, amount: float, notional: bool = False) -> bool:
        symbol = symbol.upper()
        pass

    def get_symbol_orders(self, symbol: str):
        symbol = symbol.upper()
        pass

    def get_orders(self):
        pass


class StockTrader(StockTraderADT):

    def __init__(self, trade_api: str, api_params: Dict[str, any]):
        """

        :param trade_api: Which api to use for trading. For example, alpaca may be used to begin with, but a better
        alternative may be chosen later. In which case, another if statement would need to be put into this class for
        which one to use.
        :param credentials: The parameters to be put into the API. e.g. alpaca requires an API Key ID and a Secret Key.
        """

        if not type(trade_api).__name__ == "str":
            raise ValueError("A string for the trade api should be given")

        if not type(api_params).__name__ == "dict":
            raise ValueError("A dict for the trade api parameters should be given")

        self.trade_api: str = trade_api
        self.api_params: Dict[str, any] = api_params

        # all orders made by this object
        self.orders: List[StockOrder] = []
        self.positions: Dict[str, StockPosition] = {}

        if trade_api == 'alpaca':
            self.alpaca_trader = AlpacaStockTrader(api_params)
            self.orders = self.alpaca_trader.orders

    def buy(self, symbol: str, amount: float, notional: bool = False) -> bool:

        symbol = symbol.upper()

        order_success = False

        # buy stocks using alpaca
        if self.trade_api == 'alpaca':
            try:
                order_success = self.alpaca_trader.buy(symbol, amount, notional)
            except Exception:
                pass
        return order_success

    def sell(self, symbol: str, amount: float, notional: bool = False) -> bool:

        symbol = symbol.upper()

        order_success = False

        # sell stocks which were bought using alpaca
        if self.trade_api == 'alpaca':
            try:
                order_success = self.alpaca_trader.sell(symbol, amount, notional)
            except Exception:
                pass
        return order_success

    def get_symbol_orders(self, symbol: str) -> List[StockOrder]:
        symbol = symbol.upper()
        self.orders = self.get_orders()  # update orders

        return [order for order in self.orders if order.symbol.upper() == symbol]

    def get_orders(self) -> List[StockOrder]:
        if self.trade_api == 'alpaca':
            self.orders = self.alpaca_trader.get_orders()
        return self.orders

    def get_position(self, symbol) -> StockPosition:
        if self.trade_api == 'alpaca':
            self.position = self.alpaca_trader.get_position(symbol)
        return self.position

    def get_positions(self) -> List[StockPosition]:
        if self.trade_api == 'alpaca':
            self.positions = list(self.alpaca_trader.positions)
        return self.positions
