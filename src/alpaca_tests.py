#!/usr/bin/env python

__author__ = "Ethan Posner"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0,1dev"
__maintainer__ = "Ethan Posner"
__email__ = "PosnerEthan@outlook.com"
__status__ = "Production"

import json

import alpaca_trade_api as trade_api

import trade_stocks

with open('api_conf.json', 'r') as json_file:
    api_key_json = json.load(json_file)

API_Key_ID = api_key_json['APCA_API_KEY_ID']
API_Secret_Key = api_key_json['APCA_API_SECRET_KEY']

# switch to "https://api.alpaca.markets/" for live trading
base_url = api_key_json['APCA_API_BASE_URL']

api = trade_api.REST(key_id=API_Key_ID, secret_key=API_Secret_Key, base_url=base_url)

trades = api.get_trades_iter("MSFT", "2021-02-08", "2021-02-08", limit=10)

for trade in trades:
    print(trade)

# create new stock trading object and use alpaca to do the trades
stock_trader_obj = trade_stocks.StockTrader('alpaca', (API_Key_ID, API_Secret_Key))

# buy $2.00 worth of Microsoft stocks
stock_trader_obj.buy('MSFT', amount=2, notional=True)
