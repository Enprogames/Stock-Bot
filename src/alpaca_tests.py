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

with open('api_key.json', 'r') as json_file:
    api_key_json = json.load(json_file)

API_Key_ID = api_key_json['API_Key']
API_Secret_Key = api_key_json['Secret_Key']

api = trade_api.REST(key_id=API_Key_ID, secret_key=API_Secret_Key)

trades = api.get_trades_iter("MSFT", "2021-02-08", "2021-02-08", limit=10)

for trade in trades:
    print(trade)
