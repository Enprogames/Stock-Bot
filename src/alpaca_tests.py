#!/usr/bin/env python

__author__ = "Ethan Posner"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0,1dev"
__maintainer__ = "Ethan Posner"
__status__ = "Production"

import json
import os

import trade_stocks

dir_path = os.path.dirname(os.path.realpath(__file__))
api_conf_file_str = 'api_conf.json'

with open(os.path.join(dir_path, 'api_conf.json'), 'r') as json_file:
    api_key_json = json.load(json_file)

API_Key_ID = api_key_json['APCA_API_KEY_ID']
API_Secret_Key = api_key_json['APCA_API_SECRET_KEY']

# switch to "https://api.alpaca.markets/" for live trading
BASE_URL = api_key_json['APCA_API_BASE_URL']

# create new stock trading object and use alpaca to do the trades
stock_trader_obj = trade_stocks.StockTrader('alpaca', {'APCA_API_KEY_ID': API_Key_ID, 'APCA_API_SECRET_KEY': API_Secret_Key,
                                            'APCA_API_BASE_URL': BASE_URL})


# stock_trader_obj.buy('msft', amount=5, notional=True)

# stock_trader_obj.sell('msft', amount=5, notional=True)

# print out all orders
orders = stock_trader_obj.get_orders()
for order in orders:
    print(order)

# list_orders() doesn't list filled orders?
all_orders = list(stock_trader_obj.alpaca_trader.list_orders())
filled_orders = list(stock_trader_obj.alpaca_trader.list_orders(status="filled"))

print(len(filled_orders))

for order in filled_orders:
    print(order)

print(any(order in all_orders for order in filled_orders))
