import pyupbit
import datetime
import time
from upbit_util import *

access = #ACCESS KEY
secret = #SECRET KEY

upbit = pyupbit.Upbit(access, secret)
begin_time = datetime.datetime.now()

def auto_trade(buy, ticker, runtime, low, high):
    #ticker: 거래 대상 가상화폐명
    #buy: 희망 구매 가격
    #runtime: 프로그램 기동 시간(단위: 초)
    #low: 하한 예약 매도가
    #high: 상한 예약 매도가
    
    global begin_time #프로그램 시작 당시 시간
    
    done = 0
    buy_done = 0

    show_bid(buy) #희망 매수가 출력

    while True:
        try:
            current_price = get_current_price("KRW-" + ticker)  # 반복마다의 가상화폐의 가격

            now, end_time = get_time(begin_time, runtime)  # 지금 현재 시각(now), 종료 시각(end_time)

            done_order_list, order_list = get_list(ticker) # 주문 내역

            if len(order_list) == 0 and done == 0 and done_order_list[0]['side'] == 'bid':
                print("*****************매수 체결*****************")
                done = 1

            status(low, high, current_price)

            if done == 1:
                print("매수 가격: ", done_order_list[0]['price'])
            elif done == 0:
                print("매수 가격:  매수 전(희망 매수가: " + str(buy) , " 원)")

            print("경과 시간: ", now - begin_time)

            if current_price <= low or current_price >= high:
                reserved_sell(ticker, delay, current_price)
                buy_done = 0
                done = 0
                break

            if now < end_time - datetime.timedelta(seconds=10):
                current_price = get_current_price("KRW-" + ticker)

                if buy_done == 0:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_limit_order("KRW-" + ticker, buy, (krw*0.9995) / buy)
                        print("*************매수 주문 전송*************")
                        buy_done = 1

            else:
                btc = get_balance(ticker)
                if btc > 5000 / current_price:
                    upbit.sell_market_order("KRW-" + ticker, btc * 0.9995)
                    print(str(runtime) + "초 경과, 시장가 전액 매도 체결")
                if order_list[0]['state'] == 'wait':
                    upbit.cancel_order(order_list[0]['uuid'])
                time.sleep(1)
                break

            print("---------------------------")
        except Exception as e:
            continue
            # time.sleep(1)
