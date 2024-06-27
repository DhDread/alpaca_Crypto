#imports
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import *
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import json
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import alpaca
from alpaca.data.live.crypto import *
from alpaca.data.historical.crypto import *
from alpaca.data.timeframe import *
from alpaca.trading.client import *
from alpaca.trading.stream import *
from alpaca.trading.requests import *
from alpaca.trading.enums import *
from alpaca.common.exceptions import APIError
####

# Keys
api_key = "PKICLHKLM9ZOK0KV4TP4"
secret_key = "ucBbN25orewDhySl9lQ7cHJi1vfPUlML3iI4aLWu"
paper = True # Please do not modify this. This example is for paper trading only.
trade_msg = []
trade_api_url = None
trade_api_wss = None
data_api_url = None
stream_data_wss = None
noPos = True
####
#Variables
noPos = None
client = CryptoHistoricalDataClient()
currYear = datetime.today().strftime('%Y')
currMonth = datetime.today().strftime('%m')
currDay = datetime.today().strftime('%d')
####
# Symbols
symb = ["DOGE/USD","GRT/USD","BAT/USD"]
####
#Open Client#
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=trade_api_url)
####
status = "Nothing"
x = -1
# Functions
def checkForPositions(symb, trade_client, x): #1
    try:
        symbs = symb[x].replace("/","")
        #print(symbs)
        position = trade_client.get_open_position(symbol_or_asset_id=symbs)
        #print(position)
        print("-=Position Open=-")
        status = "SELL"
        getHighLow(symb, status, x, position)
    except:
        print("-=No Position for: " + symb[x])
        status = "BUY"
        getHighLow(symb, status, x, position)

def checkForOrders(symb, x, trade_client):
    print("Symbol: " + symb[x])
    print("-=Check Orders=-")
    req = GetOrdersRequest(
        status = QueryOrderStatus.OPEN,
        symbols = [symb[x]]
        )
    orders = trade_client.get_orders(req)
    orders = str(orders).replace("[]","")
    #print(orders)
    if orders == "":
        print("-=No Orders Found=-")
        print("-=Check Positions=-")
        checkForPositions(symb, trade_client, x)
    else:
        print("-=Order Pending=-")   
         
def getHighLow(symb, status, x, position): #3
    request_params = CryptoBarsRequest(
                        symbol_or_symbols=[symb[x]],
    timeframe=TimeFrame.Day,
    start=datetime(int(currYear),int(currMonth),int(currDay))
    )
    bars = client.get_crypto_bars(request_params)
    bars_string = str(bars)
    #print(bars_string)
    bars_replace = bars_string.replace(" ","|")
    bars_split = bars_replace.split("|")
    bars_replace = str(bars_split).replace("''","")
    bars_replace = str(bars_replace).replace(",","")
    bars_replace = str(bars_replace).replace(r"\n'","")
    bars_replace = str(bars_replace).replace(r"    ","|")
    bars_replace = str(bars_replace).split("|")
    High_replace = str(bars_replace[1]).replace(r"high","")
    High_replace = str(High_replace).replace(r"'':","")
    High_replace = str(High_replace).replace(" '","")
    High_replace = str(High_replace).replace(r'""',"")
    highPrice = float(High_replace)
    Low_replace = str(bars_replace[2]).replace(r"low","")
    Low_replace = str(Low_replace).replace(r"'':","")
    Low_replace = str(Low_replace).replace(" '","")
    lowPrice = str(Low_replace).replace(r'""',"")
    #print(highPrice) #High Price
    #print(lowPrice) #Low Price
    rangeSize = float(highPrice) - float(lowPrice)
    #print("range: " + str(rangeSize))
    if status == "BUY":
        print("Buy: " + "StopLoss: " + str(float(highPrice) - float(rangeSize)))
        print("Buy: " + "TakeProf: " + str(float(highPrice) + float(rangeSize)))
    elif status == "SELL":
        print("Sell: " + "StopLoss: " + str(float(lowPrice) + float(rangeSize)))
        print("Sell: " + "TakeProf: " + str(float(lowPrice) - float(rangeSize)))
    #print(status)
    orderBuySell(status, highPrice, lowPrice, rangeSize, symb, x, position)

def orderBuySell(status, highPrice, lowPrice, rangeSize, symb, x, position): #4
    # stop limit order
    #print(symb[x])
    #print(status)
    if status == "SELL":
        #Get amount to sell
        position_string = str(position)
        position_replace = position_string.replace(" ","|")
        position_split = position_replace.split("|")
        qty = position_split[8].split("'")[1]
        print(qty)
        # Sell
        req = StopLimitOrderRequest(
                    symbol = symb[x],
                    qty = qty,
                    side = OrderSide.SELL,
                    time_in_force = TimeInForce.GTC,
                    limit_price = str(float(lowPricePrice) - float(rangeSize)),
                    stop_price = str(float(lowPricePrice) + float(rangeSize))
                    )
        #res = trade_client.submit_order(req)
        #print(res)
        print(status + " Purchased Sell Order")
        status = "Nothing"
    if status == "BUY":
        req = StopLimitOrderRequest(
                    symbol = symb[x],
                    qty = 100,
                    side = OrderSide.BUY,
                    time_in_force = TimeInForce.GTC,
                    limit_price = str(float(highPrice) + float(rangeSize)),
                    stop_price = str(float(highPrice) - float(rangeSize))
                    )
        #res = trade_client.submit_order(req)
        #print(res)
        print(status + " Purchased Buy Order")
        status = "Nothing"
    #highPrice = 0
    #lowPrice = 0
    #rangeSize = 0

def returnw():
    return 1





while True:
    x+=1
    print("-=-----=-")
    #checkForPositions(symb, trade_client, status, x) #1
    checkForOrders(symb, x, trade_client)
    if x == 2:
        x=-1
    now = datetime.now()
    print("-=-----=-")
    print(now)
    print("-=-----=-")
    time.sleep(15)






# ------------- N/A ----------------- 
#f"""
#def getLastTrades(symb,x):
#    req = CryptoLatestQuoteRequest(
#        symbol_or_symbols = [symb[x]],
#    )
#    res = client.get_crypto_latest_quote(req)
###    res_string = str(res)
  #  res_replace = res_string.replace(" ","|")
  ##  res_split = res_replace.split("|")
 # 3 res_replace = str(res_split).replace("''","")
   # res_replace = str(res_replace).replace(",","")
   # res_replace = str(res_replace).replace(r"\n'","")
   ### res_replace = str(res_replace).replace(r"    ","|")
  #  res_replace = str(res_replace).split("|")
  #  # ask price cleanup
 #   AP_replace = str(res_replace[1]).replace(r"ask_price","")
  #  AP_replace = str(AP_replace).replace(r"'':","")
 #   AP_replace = str(AP_replace).replace(" '","")
 #   AP_replace = str(AP_replace).replace(r'""',"")
  #  askPrice = float(AP_replace)
 #   # bid price cleanup
 #   BP_replace = str(res_replace[4]).replace(r"bid_price","")
  #  BP_replace = str(BP_replace).replace(r"'':","")
 #   BP_replace = str(BP_replace).replace(" '","")
  #  BP_replace = str(BP_replace).replace(r'""',"")
  #  bidPrice = float(BP_replace)
#   quoteAvg = float(askPrice + bidPrice) / 2
  #  #prints
    #print(res_replace)
  #  print(askPrice) #Ask Price
  #  print(bidPrice) #Bid Price
  #  print("Average: " + str(quoteAvg))
    
#def checkIfBuySell(orders):
 #   print(orders)
 #   orders_string = str(orders)
    #print(bars_string)
 #   orders_replace = orders_string.replace(" ","|")
  #  orders_split = orders_replace.split("|")
  #  orders_replace = str(orders_split).replace("''","")
  #  orders_replace = str(orders_replace).replace(",","")
  #  orders_replace = str(orders_replace).replace(r"\n'","")
   # orders_replace = str(orders_replace).replace(r"    ","|")
   # orders_replace = str(orders_replace).split("|")
   # print(orders_replace[15])
  # """
