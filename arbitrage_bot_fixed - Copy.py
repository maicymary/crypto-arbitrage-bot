# Save as arbitrage_bot_secure.py

import csv
import time
import os
from datetime import datetime
import requests
import ccxt
from dotenv import load_dotenv

# ------------------ Load Environment Variables ------------------
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET")
MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_SECRET = os.getenv("MEXC_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ------------------ Initialize Exchanges ------------------
binance = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET,
    'enableRateLimit': True,
})

mexc = ccxt.mexc({
    'apiKey': MEXC_API_KEY,
    'secret': MEXC_SECRET,
    'enableRateLimit': True,
})

# ------------------ Telegram ------------------
def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("⚠️ Telegram not configured")
        return

    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")

send_telegram_message("✅ Bot started. Monitoring for arbitrage opportunities.")

# ------------------ Price Fetchers ------------------
def get_binance_price(symbol):
    try:
        return binance.fetch_ticker(symbol)['last']
    except:
        print(f"⚠️ Binance price error: {symbol}")
        return None

def get_mexc_price(symbol):
    try:
        return mexc.fetch_ticker(symbol)['last']
    except:
        print(f"⚠️ MEXC price error: {symbol}")
        return None

# ------------------ Helpers ------------------
def get_mexc_balance():
    try:
        balance = mexc.fetch_free_balance()
        return balance.get('USDT', 0)
    except Exception as e:
        print(f"Error fetching MEXC balance: {e}")
        return 0

# ------------------ Trade Actions ------------------
def place_buy_order_mexc(symbol, amount):
    try:
        return mexc.create_market_buy_order(symbol, amount)
    except Exception as e:
        send_telegram_message(f"❌ MEXC Buy Error: {e}")
        return None

def place_sell_order_binance(symbol, amount):
    try:
        return binance.create_market_sell_order(symbol, amount)
    except Exception as e:
        send_telegram_message(f"❌ Binance Sell Error: {e}")
        return None

# ------------------ Arbitrage Logic ------------------
def check_arbitrage(symbol):
    binance_price = get_binance_price(symbol)
    mexc_price = get_mexc_price(symbol)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if binance_price is None or mexc_price is None:
        return

    print(f"{symbol} → Binance: ${binance_price:.4f}, MEXC: ${mexc_price:.4f}")

    if mexc_price < binance_price:
        profit = binance_price - mexc_price

        # basic fee buffer (~0.1% each side)
        if profit > (binance_price * 0.002):
            msg = f"[{now}]\n📉 Arbitrage Opportunity!\nBuy {symbol} on MEXC at ${mexc_price:.4f}, Sell on Binance at ${binance_price:.4f}\nProfit: ${profit:.4f}"
            print(msg)
            send_telegram_message(msg)

            usdt_balance = get_mexc_balance()
            if usdt_balance < 5:
                send_telegram_message("⚠️ Insufficient USDT on MEXC.")
                return

            trade_amount = round(5 / mexc_price, 5)
            order = place_buy_order_mexc(symbol, trade_amount)
            if order:
                place_sell_order_binance(symbol, trade_amount)

# ------------------ Main Loop ------------------
symbols = ["BTC/USDT", "XRP/USDT", "DOGE/USDT"]
available_symbols = []

for sym in symbols:
    try:
        mexc.fetch_ticker(sym)
        available_symbols.append(sym)
    except:
        print(f"⛔ {sym} NOT supported by MEXC.")

while True:
    for coin in available_symbols:
        check_arbitrage(coin)
    time.sleep(15)# Save this script as arbitrage_bot_4pm_version.py

import csv
import time
import os
from datetime import datetime
import requests
import ccxt

# ------------------ Initialize Exchanges ------------------
binance = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET,
    'enableRateLimit': True,
})

mexc = ccxt.mexc({
    'apiKey': MEXC_API_KEY,
    'secret': MEXC_SECRET,
    'enableRateLimit': True,
})

# ------------------ Telegram ------------------
TELEGRAM_TOKEN = '7657086810:AAHdobO2EmtFCYREbVx7BqGI9xAo7uLaBr4'
CHAT_ID = '1195581551'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")

send_telegram_message("✅ Bot started. Monitoring for arbitrage opportunities.")

# ------------------ Price Fetchers ------------------
def get_binance_price(symbol):
    try:
        return binance.fetch_ticker(symbol)['last']
    except:
        print(f"⚠️ Binance price error: {symbol}")
        return None

def get_mexc_price(symbol):
    try:
        return mexc.fetch_ticker(symbol)['last']
    except:
        print(f"⚠️ MEXC price error: {symbol}")
        return None

# ------------------ Helpers ------------------
def format_symbol(symbol):
    return symbol.replace("/", "")

def get_mexc_balance():
    try:
        balance = mexc.fetch_free_balance()
        return balance.get('USDT', 0)
    except Exception as e:
        print(f"Error fetching MEXC balance: {e}")
        return 0

# ------------------ Trade Actions ------------------
def place_buy_order_mexc(symbol, amount):
    try:
        return mexc.create_market_buy_order(symbol, amount)
    except Exception as e:
        send_telegram_message(f"❌ MEXC Buy Error: {e}")
        return None

def place_sell_order_binance(symbol, amount):
    try:
        return binance.create_market_sell_order(symbol, amount)
    except Exception as e:
        send_telegram_message(f"❌ Binance Sell Error: {e}")
        return None

# ------------------ Arbitrage Logic ------------------
def check_arbitrage(symbol):
    binance_price = get_binance_price(symbol)
    mexc_price = get_mexc_price(symbol)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if binance_price is None or mexc_price is None:
        return

    print(f"{symbol} → Binance: ${binance_price:.4f}, MEXC: ${mexc_price:.4f}")

    if mexc_price < binance_price:
        profit = binance_price - mexc_price
        if profit > 0.05:
            msg = f"[{now}]\n📉 Arbitrage Opportunity!\nBuy {symbol} on MEXC at ${mexc_price:.4f}, Sell on Binance at ${binance_price:.4f}\nProfit: ${profit:.4f}"
            print(msg)
            send_telegram_message(msg)

            usdt_balance = get_mexc_balance()
            if usdt_balance < 5:
                send_telegram_message("⚠️ Insufficient USDT on MEXC to place order.")
                return

            trade_amount = round(5 / mexc_price, 5)
            order = place_buy_order_mexc(symbol, trade_amount)
            if order:
                place_sell_order_binance(symbol, trade_amount)

# ------------------ Main Loop ------------------
symbols = ["BTC/USDT", "XRP/USDT", "DOGE/USDT"]
available_symbols = []

for sym in symbols:
    try:
        mexc.fetch_ticker(sym)
        available_symbols.append(sym)
    except:
        print(f"⛔ {sym} NOT supported by MEXC. Removing.")

while True:
    for coin in available_symbols:
        check_arbitrage(coin)
    time.sleep(15)
