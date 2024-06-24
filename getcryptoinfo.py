from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

# no keys required for crypto data
client = CryptoHistoricalDataClient()
currYear = datetime.today().strftime('%Y')
currMonth = datetime.today().strftime('%m')
currDay = datetime.today().strftime('%d')
 
import requests

url = "https://data.alpaca.markets/v1beta3/crypto/us/latest/trades?symbols=DOGE%2FUSD"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)

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

print(bars.df)



