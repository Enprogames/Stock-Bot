#!/usr/bin/env python

__author__ = "Ethan Posner"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0,1dev"
__maintainer__ = "Ethan Posner"
__status__ = "Production"

import json

import alpaca_trade_api as trade_api

with open('api_conf.json', 'r') as json_file:
    api_key_json = json.load(json_file)

API_Key_ID = api_key_json['APCA_API_KEY_ID']
API_Secret_Key = api_key_json['APCA_API_SECRET_KEY']

# switch to "https://api.alpaca.markets/" for live trading
base_url = api_key_json['APCA_API_BASE_URL']

api = trade_api.REST(key_id=API_Key_ID, secret_key=API_Secret_Key, base_url=base_url)

trades = api.list_orders()

for trade in trades:
    print(trade)
