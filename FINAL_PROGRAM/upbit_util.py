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


def reserved_sell(ticker, current_price):
    btc = get_balance(ticker)

    if btc > 5000 / current_price:
        upbit.sell_market_order("KRW-" + ticker, btc * 0.9995)
        print("##################예약 매도 체결##################")
        time.sleep(delay)


def get_time(begin_time, runtime):
    return datetime.datetime.now(), begin_time + datetime.timedelta(seconds=runtime + 10)


def get_list(ticker):
    return upbit.get_order("KRW-" + ticker, state="done"), upbit.get_order("KRW-" + ticker)
