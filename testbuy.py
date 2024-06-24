import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import alpaca
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.live.crypto import *
from alpaca.data.historical.crypto import *
from alpaca.data.requests import *
from alpaca.data.timeframe import *
from alpaca.trading.client import *
from alpaca.trading.stream import *
from alpaca.trading.requests import *
from alpaca.trading.enums import *
from alpaca.common.exceptions import APIError

# Please change the following to your own PAPER api key and secret
# You can get them from https://alpaca.markets/

api_key = "PKICLHKLM9ZOK0KV4TP4"
secret_key = "ucBbN25orewDhySl9lQ7cHJi1vfPUlML3iI4aLWu"

#### We use paper environment for this example ####
paper = True # Please do not modify this. This example is for paper trading only.
####

#Buy This Symbol ---
symb = ["DOGEUSD","GRTUSD","BATUSD"]
#symb = "DOGE/USD"
#**
trade_msg = []
# Below are the variables for development this documents
# Please do not change these variables
trade_api_url = None
trade_api_wss = None
data_api_url = None
stream_data_wss = None
noPos = True
#print("Alpaca-PY Version:" + " " + alpaca.__version__)
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=trade_api_url)

# ref. https://docs.alpaca.markets/docs/orders-at-alpaca
# ref. https://docs.alpaca.markets/reference/postorder
x = -1
while True:
    x+=1
    #print(x)
    try:
        position = trade_client.get_open_position(symbol_or_asset_id=symb[x])
        #print(position)
    except:
        print("-No " + symb[x] +" Currently-")
        print("-=Purchasing=-")
        noPos = False
        print(noPos)
        #print(position)
        
    if noPos == True:
        position_string = str(position)
        position_replace = position_string.replace(" ","|")
        position_split = position_replace.split("|")
        currGL = (float(position_split[17].split("'")[1]) - float(position_split[7].split("'")[1])) * 0.9975
        currVal = float(position_split[8].split("'")[1]) * float(position_split[7].split("'")[1])
        currMVal = (float(position_split[7].split("'")[1]) * float(position_split[8].split("'")[1]))*.9975
        print("Symb" + "       " 
            + "Qty" + "       " 
            + "Purchased" + "      " 
            + "CurrPrice" + "     "
            + "Gain/Loss" + "                "
            + "CurrVal" + "                   "
            + "CurrMVal")
        print(position_split[1].split("'")[1] + "   " 
            + position_split[8].split("'")[1] + "      "
            + position_split[7].split("'")[1] + "        "
            + position_split[17].split("'")[1] + "       "
            + str(currGL) + "    "
            + str(currVal) + "       "
            + str(currMVal*.9975))
    else:
    #Buy
        req = MarketOrderRequest(
            symbol = symb[x],
            qty = "100",
            side = OrderSide.BUY,
            type = OrderType.MARKET,
            time_in_force = TimeInForce.GTC,
        )
        buy = trade_client.submit_order(req)
        print(buy)
    try:   
        if currGL > 0.0025:  
#sell
            req = MarketOrderRequest(
                symbol = symb[x],
                qty = float(position_split[8].split("'")[1]),
                side = OrderSide.SELL,
                type = OrderType.MARKET,
                time_in_force = TimeInForce.GTC,
            )
            sell = trade_client.submit_order(req)
            print("-=Selling=-")
            print(sell)
    except:
        print("-Waiting-")
    if x == 2:
        x=-1
    noPos = True
    time.sleep(7)




