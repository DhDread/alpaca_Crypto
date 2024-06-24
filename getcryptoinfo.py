from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

# no keys required for crypto data
client = CryptoHistoricalDataClient()
currYear = datetime.today().strftime('%Y')
currMonth = datetime.today().strftime('%m')
currDay = datetime.today().strftime('%d')
 
# get latest quotes by symbol
req = CryptoLatestQuoteRequest(
    symbol_or_symbols = ["BAT/USD"],
)
res = client.get_crypto_latest_quote(req)
res_string = str(res)
res_replace = res_string.replace(" ","|")
res_split = res_replace.split("|")
res_replace = str(res_split).replace("''","")
res_replace = str(res_replace).replace(",","")
res_replace = str(res_replace).replace(r"\n'","")
res_replace = str(res_replace).replace(r"    ","|")
res_replace = str(res_replace).split("|")
# ask price cleanup
AP_replace = str(res_replace[1]).replace(r"ask_price","")
AP_replace = str(AP_replace).replace(r"'':","")
AP_replace = str(AP_replace).replace(" '","")
AP_replace = str(AP_replace).replace(r'""',"")
askPrice = float(AP_replace)
# bid price cleanup
BP_replace = str(res_replace[4]).replace(r"bid_price","")
BP_replace = str(BP_replace).replace(r"'':","")
BP_replace = str(BP_replace).replace(" '","")
BP_replace = str(BP_replace).replace(r'""',"")
bidPrice = float(BP_replace)
#prints
print(res_replace)
print(askPrice) #Ask Price
print(bidPrice) #Bid Price
print("Average: " + str((askPrice + bidPrice) / 2))











#Bars

request_params = CryptoBarsRequest(
                        symbol_or_symbols=[
"AAVE/USD",
"AVAX/USD",
"BAT/USD",
"BCH/USD",
"BTC/USD",
"CRV/USD",
"DOGE/USD",
"DOT/USD",
"ETH/USD",
"GRT/USD",
"LINK/USD",
"LTC/USD",
"MKR/USD",
"SHIB/USD",
"SUSHI/USD",
"UNI/USD",
"USDC/USD",
"USDT/USD",
"XTZ/USD",
"YFI/USD"
],
timeframe=TimeFrame.Day,
start=datetime(int(currYear),int(currMonth),int(currDay))
)

bars = client.get_crypto_bars(request_params)

#print(bars.df)



