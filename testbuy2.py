import json
import logging
import threading
from time import *
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import alpaca
from alpaca.data.live.crypto import *
from alpaca.data.historical.crypto import *
from alpaca.data.requests import *
from alpaca.data.timeframe import *
from alpaca.trading.client import *
from alpaca.trading.stream import *
from alpaca.trading.requests import *
from alpaca.trading.enums import *
from alpaca.common.exceptions import APIError

# init
logging.basicConfig(
    filename='errlog.log',
    level=logging.WARNING,
    format='%(asctime)s:%(levelname)s:%(message)s',
)
api_key = "PKICLHKLM9ZOK0KV4TP4"
secret_key = "ucBbN25orewDhySl9lQ7cHJi1vfPUlML3iI4aLWu"
paper = True # Please do not modify this. This example is for paper trading only.
####

# Below are the variables for development this documents
# Please do not change these variables
trade_api_url = None
trade_api_wss = None
data_api_url = None
stream_data_wss = None
#print("Alpaca-PY Version:" + " " + alpaca.__version__)
trade_client = TradingClient(api_key=api_key, secret_key=secret_key, paper=paper, url_override=trade_api_url)


trade_msg = []
order_msg = []
past_trades = []

searching_for_trade = False
order_sent = False
order_submitted = False
active_trade = False
done_for_the_day = False

# check if market is open
#api.cancel_all_orders()
#clock = api.get_clock()

#if clock.is_open:
#    pass
#else:
#    time_to_open = clock.next_open - clock.timestamp
#    sleep(time_to_open.total_seconds())
#
#if len(api.list_positions()) == 0:
 #   searching_for_trade = True
#else:
 #   active_trade = True

# init WebSocket
conn = tradeapi.stream.Stream(api_key, api_secret, base_url)


#@conn.on(r'^account_updates$')
async def on_account_updates(conn, channel, account):
    order_msg.append(account)


#@conn.on(r'^trade_updates$')
async def on_trade_updates(conn, channel, trade):
    trade_msg.append(trade)
    if 'fill' in trade.event:
        past_trades.append(
            [
                trade.order['updated_at'],
                trade.order['symbol'],
                trade.order['side'],
                trade.order['filled_qty'],
                trade.order['filled_avg_price'],
            ]
        )
        with open('past_trades.csv', 'w') as f:
            json.dump(past_trades, f, indent=4)
        print(past_trades[-1])


def ws_start():
    conn.run(['account_updates', 'trade_updates'])


# start WebSocket in a thread
ws_thread = threading.Thread(target=ws_start, daemon=True)
ws_thread.start()
sleep(10)


# functions
def time_to_market_close():
    clock = api.get_clock()
    closing = clock.next_close - clock.timestamp
    return round(closing.total_seconds() / 60)


def send_order(direction):
    if time_to_market_close() > 20:
        if direction == 'buy':
            sl = high - range_size
            tp = high + range_size
        elif direction == 'sell':
            sl = low + range_size
            tp = low - range_size

        api.submit_order(
            symbol='AAPL',
            qty=100,
            side=direction,
            type='market',
            time_in_force='day',
            order_class='bracket',
            stop_loss=dict(stop_price=str(sl)),
            take_profit=dict(limit_price=str(tp)),
        )
        return True, False

    else:
        return False, True


# main loop
while True:

    try:

        candlesticks = api.get_barset('AAPL', 'minute', limit=10)
        high = candlesticks['AAPL'][0].h
        low = candlesticks['AAPL'][0].l
        range_size = high - low
        if range_size / candlesticks['AAPL'][0].c < 0.003:
            range_size = candlesticks['AAPL'][0].c * 0.003
        for candle in candlesticks['AAPL']:
            if candle.h > high:
                high = candle.h
            elif candle.l < low:
                low = candle.l
        range_size = high - low

        while searching_for_trade:
            clock = api.get_clock()
            sleep(60 - clock.timestamp.second)
            candlesticks = api.get_barset('AAPL', 'minute', limit=1)
            if candlesticks['AAPL'][0].c > high:
                searching_for_trade = False
                order_sent, done_for_the_day = send_order('buy')

            elif candlesticks['AAPL'][0].c < low:
                searching_for_trade = False
                order_sent, done_for_the_day = send_order('sell')

        while order_sent:
            sleep(1)
            for item in trade_msg:
                if item.event == 'new':
                    order_submitted = True
                    order_sent = False

        while order_submitted:
            sleep(1)
            for item in trade_msg:
                if item.order['filled_qty'] == '100':
                    order_submitted = False
                    active_trade = True
                    trade_msg = []

        while active_trade:
            for i in range(time_to_market_close() - 5):
                sleep(60)
                if len(api.list_positions()) == 0:
                    active_trade = False
                    searching_for_trade = True
                    break
            if active_trade:
                done_for_the_day = True
                active_trade = False

        while done_for_the_day:
            api.close_all_positions()
            clock = api.get_clock()
            next_market_open = clock.next_open - clock.timestamp
            sleep(next_market_open.total_seconds())
            searching_for_trade = True

    except Exception as e:
        logging.exception(e)