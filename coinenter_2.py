import time
import pyupbit
import datetime
import numpy as np

access = "kFKBL6DDvVWZPmZxaTnI2YVzxOwxLVgf9aLNYkNX"
secret = "RkM8Irspe5QVVXB8Ld2w8I3ULHWQeYlROx8D0jsx"


def get_target_price(ticker, ror):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + \
        (df.iloc[0]['high'] - df.iloc[0]['low']) * ror
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


coin_list = pyupbit.get_tickers(fiat="KRW")
coin_list.remove("KRW-BTT")

def get_ror(k=0.5):
    df = pyupbit.get_ohlcv(coin_list[i], count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)
    ror = df['ror'].cumprod()[-2]
    return ror
# 자동매매 시작
while True:
    try:
        i = 0
        while i < len(coin_list):
        # for i in range(len(coin_list)):
            cl = coin_list[i]
            coin_list_str = str(cl)
            coin_list_str = coin_list_str[4:(len(coin_list_str) + 1)]
            temp_coin_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            ror_max = 0.1
            for j in range(len(temp_coin_list)):
                if get_ror(ror_max) < get_ror(temp_coin_list[j]):
                    ror_max = temp_coin_list[j]
            now = datetime.datetime.now()
            print(now)
            start_time = get_start_time(cl)
            end_time = start_time + datetime.timedelta(days=1)
            if start_time < now < end_time - datetime.timedelta(minutes=60): #9시 ~ 8시 59분이면 True
                target_price = get_target_price(cl, ror_max)    
                current_price = get_current_price(cl)
                if target_price < current_price:
                    if current_price < target_price * 1.001 or current_price < target_price + 1 :
                        krw = get_balance("KRW")
                        if krw > 5000:
                            upbit.buy_market_order(cl, krw*0.9995)
                if current_price > (target_price * 1.1):
                    btc = get_balance(coin_list_str)
                    upbit.sell_market_order(ticker = cl, volume = btc*0.9995)

            else: # 8시 59분 ~ 8시 59분 59초면 작동
                btc = get_balance(coin_list_str)
                if btc > 5000 / get_current_price(cl):
                    upbit.sell_market_order(ticker = cl, volume = btc*0.9995)
            time.sleep(0.1)
            i += 1
    except Exception as e:
        print(e)
        time.sleep(1)
