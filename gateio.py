""" 
 * ------------------------------------------------------------
 * "THE BEERWARE LICENSE" (Revision 42):
 * Onat Deniz Dogan <oddogan@protonmail.com> wrote this code. As long as you retain this 
 * notice, you can do whatever you want with this stuff. If we
 * meet someday, and you think this stuff is worth it, you can
 * buy me a beer in return.
 * ------------------------------------------------------------
"""

import ccxt, time
import utils.config
from utils.telegram_bot import post_message

# Create the GateIO exchange object using CCXT
exchange = ccxt.gateio({
    'apiKey': utils.config.GATEIO_API_KEY,
    'secret': utils.config.GATEIO_SECRET_KEY,
})

# Get the market and balance data from GateIO
markets = exchange.fetch_markets()
balance = exchange.fetch_total_balance()

# Get all the available symbols from GateIO
symbols = [symbol for symbol in [market['symbol'] for market in markets]]

# Placeholder for keeping the price at the time of buying
entryPrice = 0

def symbol_check(symbol):
    if symbol in symbols:
        print(f"Good news!, {symbol} exists in Gate.io")
        return True
    else:
        print(f"Sorry, {symbol} does not exist in Gate.io")
        return False

def buy(symbol):
    global entryPrice

    # Pick a price more than the last ticker data, to make sure that we can fulfill order
    price = exchange.fetch_ticker(symbol)['last'] * 1.01
    entryPrice = price

    # Get the current USDT balance in GateIO
    balance = exchange.fetch_total_balance()
    coin = symbol.split('/')[0]
    usdt_balance = balance['USDT']

    # Calculate the amount of coin that we can buy, apply a small margin for rounding errors in balance
    amount = (usdt_balance * 0.999) / (price)

    # Create the limit buy order
    exchange.create_limit_buy_order(symbol, amount=amount, price=price)

    # Notify the user both on Telegram and CLI
    message = f"You have {usdt_balance} USDT in your account. Buying {amount} {coin} for {price}"
    print(message)
    post_message(message)

def sell(symbol):

    # Pick a price less than the last ticker data, to make sure that we can fulfill order
    price = exchange.fetch_ticker(symbol)['last'] * 0.99

    # Get the current coin balance in GateIO
    balance = exchange.fetch_total_balance()
    coin = symbol.split('/')[0]
    coin_balance = balance[coin]

    # Create the limit sell order
    exchange.create_limit_sell_order(symbol, amount=coin_balance, price=price)

    # Notify the user both on Telegram and CLI
    message = f"You have {coin_balance} {coin} in your account. Selling them for {price}"
    print(message)
    post_message(message)

    
def sellBearish(symbol):
    global entryPrice
    bestPrice = exchange.fetch_ticker(symbol)['last']
    balance = exchange.fetch_total_balance()

    while True:
        price = exchange.fetch_ticker(symbol)['last']

        # Update the best price if we have a new best price
        if price > bestPrice:
            bestPrice = price

        # If the price has dropped 3% percent w.r.t. the best price, sell the coins and get the profit
        elif price < (0.97 * bestPrice):
            coin = symbol.split('/')[0]
            coin_balance = balance[coin]

            exchange.create_limit_sell_order(symbol, amount=coin_balance, price=price*0.99)

            # Notify the user both on Telegram and CLI
            message = f"You have {coin_balance} {coin} in your account.\nSelling them for {price*0.99}\nYour profit is{price/entryPrice*100}"
            print(message)
            post_message(message)