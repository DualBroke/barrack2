import time
import pyupbit
import datetime

access = "H1daculIk3hJlFiaxbPTcdkRUdLX5xq1B7SFYIDS"
secret = "dW6fFteihFuSXMVMnIaMUE32tHRhTJ6E0sFkV1Zv"


def get_sum_DOGE_price():
    sum_DOGE_price = get_balance("DOGE") * get_current_price("KRW-DOGE")
    return sum_DOGE_price


def get_sum_BTC_price():
    sum_BTC_price = get_balance("BTC") * get_current_price("KRW-BTC")
    return sum_BTC_price


def get_sum_TFUEL_price():
    sum_TFUEL_price = get_balance("TFUEL") * get_current_price("KRW-TFUEL")
    return sum_TFUEL_price


def get_sum_ETH_price():
    sum_ETH_price = get_balance("ETH") * get_current_price("KRW-ETH")
    return sum_ETH_price


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + \
        (df.iloc[0]['high'] - df.iloc[0]['low']) * k
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
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
n = 1
n2 = 0
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        print(now)
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.9)
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price < (target_price * 1.001):
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    at_that_time = get_current_price("KRW-BTC")
                    btc = get_balance("BTC")
                    if btc > 5000 / get_current_price("KRW-BTC"):
                        if get_current_price("KRW-BTC") > target_price * 1.05:
                            upbit.sell_market_order(
                                "KRW-BTC", btc)

        else:
            if btc > 5000 / get_current_price("KRW-BTC"):
                upbit.sell_market_order("KRW-BTC", btc)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
