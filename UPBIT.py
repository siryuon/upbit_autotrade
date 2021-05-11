import pyupbit
import datetime

access = #ACCESS KEY
secret = #SECRET KEY

upbit = pyupbit.Upbit(access, secret)

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]

    return start_time

def get_balance(ticker):
    balances = upbit.get_balances()

    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

begin_time = datetime.datetime.now()

def auto_trade():
    global begin_time
    
    while True:
        print("try trading")
        try:
            now = datetime.datetime.now()
            end_time = begin_time + datetime.timedelta(seconds=30)
            
            if now < end_time - datetime.timedelta(seconds=10):
                target_price = #TARGET PRICE
                current_price = get_current_price("KRW-BTC")

                if target_price < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order("KRW-BTC", krw*0.9995)
            else:
                btc = get_balance("BTC")
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)

                time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(1)
            
auto_trade()
