"""
import pyRofex
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import time

instrument = "DLR/JUN24"

# Create empty DataFrame to store MarketData
prices = pd.DataFrame(columns=["Time", "Bid", "Offer", "Last"])
prices.set_index('Time', inplace=True)

plt.ion()
fig, ax = plt.subplots(figsize=(14, 5))
count = 0

# Initialize the environment
pyRofex.initialize(user="oadricabrera9893",
                   password="dkjtoG2@",
                   account="REM9893",
                   environment=pyRofex.Environment.REMARKET)


def update_plot():
    global ax, prices, count
    if len(prices.index) > count:
        count = len(prices.index)
        ax.clear()
        plt.title('Price %s' % instrument, fontsize=15)
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        prices.plot(kind='line', y='Bid', lw=1.5, color='b', label='Bid Price', ax=ax)
        prices.plot(kind='line', y='Offer', lw=1.5, color='g', label='Offer Price', ax=ax)
        prices.plot(kind='line', y='Last', lw=1.5, marker='.', color='r', label='Last Price', ax=ax)
        ax.grid(True, linestyle='--')
        plt.tight_layout()
        plt.legend()
        plt.draw()
        plt.pause(0.2)


# Defines the handlers that will process the messages
def market_data_handler(message):
    global prices
    print("Market Data Message Received: {0}".format(message))
    try:
        bid_price = message["marketData"]["BI"][0]["price"] if "BI" in message["marketData"] else None
        offer_price = message["marketData"]["OF"][0]["price"] if "OF" in message["marketData"] else None
        last_price = message["marketData"]["LA"]["price"] if "LA" in message["marketData"] else None
        timestamp = datetime.fromtimestamp(message["timestamp"] / 1000)
        prices.loc[timestamp] = [bid_price, offer_price, last_price]
    except Exception as e:
        print(f"Error processing market data: {e}")


# Initialize Websocket Connection with the handlers
pyRofex.init_websocket_connection(market_data_handler=market_data_handler)

# Subscribes to receive market data messages
pyRofex.market_data_subscription(
    tickers=[instrument],
    entries=[
        pyRofex.MarketDataEntry.BIDS,
        pyRofex.MarketDataEntry.OFFERS,
        pyRofex.MarketDataEntry.LAST]
)

while True:
    update_plot()
    time.sleep(0.5)

"""
import pyRofex

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import time

instrument = "DLR/JUL25"

# Create empty DataFrame to store MarketData
prices = pd.DataFrame(columns=["Time", "Bid", "Offer", "Last"])  
prices.set_index('Time', inplace=True)  

plt.ion()
fig, ax = plt.subplots(figsize=(14, 5))
count = 0

# Initialize the environment
pyRofex.initialize(user="oadricabrera20096",
                   password="nvdevU6$",
                   account="REM20096",
                   environment=pyRofex.Environment.REMARKET)


def update_plot():
    global ax, prices, count
    if len(prices.index) > count:
        count = len(prices.index)
        ax.clear()
        plt.title('Price %s' % instrument, fontsize=15)
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        prices.plot(kind='line', y='Bid', lw=1.5, color='b', label='Bid Price', ax=ax)
        prices.plot(kind='line', y='Offer', lw=1.5, color='b', label='Offer Price', ax=ax)
        prices.plot(kind='line', y='Last', lw=1.5, marker='.', color='r', label='Last Price', ax=ax)
        ax.grid(True, linestyle='--')
        plt.tight_layout()
        plt.draw()
        plt.pause(0.2)


# Defines the handlers that will process the messages
def market_data_handler(message):
    global prices
    print("Market Data Message Received: {0}".format(message))
    last = None if not message["marketData"]["LA"] else message["marketData"]["LA"]["price"]
    prices.loc[datetime.fromtimestamp(message["timestamp"]/1000)] = [
        message["marketData"]["BI"][0]["price"],
        message["marketData"]["OF"][0]["price"],
        last
    ]


# Initialize Websocket Connection with the handlers
pyRofex.init_websocket_connection(market_data_handler=market_data_handler)


# Subscribes to receive market data messages
pyRofex.market_data_subscription(
    tickers=[instrument],
    entries=[
        pyRofex.MarketDataEntry.BIDS,
        pyRofex.MarketDataEntry.OFFERS,
        pyRofex.MarketDataEntry.LAST]
)

while True:
    update_plot()
    time.sleep(0.5)






# métodos

# get_detailed_instruments al iniciar el script
# get_detailed_position cada 5 segundos
# get_account_report cada 5 segundos

# wS

# init_websocket_connection
# send_order_via_websocket
# cancel_order_via_websocket
# order_report_subscription
# market_data_subscription