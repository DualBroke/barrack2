import time
import pyupbit
import datetime
import numpy as np
# import coin_list as cl

access = "iqDrPCK1qbAsZyXxHllNGNPYxqTzSlsD7931ve3G"
secret = "BtY10ZFwrPakQFUEYj4S5BxeLfQ9O06dbmjxL4eO"

list = ["KRW-DOGE", "KRW-BTC", "KRW-ETH", "KRW-STEEM", "KRW-GMT", "KRW-TRX", "KRW-XRP", "KRW-KNC", "KRW-NEAR", "KRW-NU", "KRW-BORA", "KRW-WAVES", "KRW-ZIL", "KRW-STX", "KRW-JST", "KRW-MTL", "KRW-AXS", "KRW-KAVA", "KRW-ZRX", "KRW-DAWN", "KRW-CVC", "KRW-SAND", "KRW-GRS", "KRW-WEMIX", "KRW-MBL", "KRW-EOS", "KRW-SOL", "KRW-PUNDIX", "KRW-ETC", "KRW-FLOW", "KRW-VET", "KRW-MATIC", "KRW-ADA", "KRW-ALGO", "KRW-HUM", "KRW-MFT", "KRW-MANA", "KRW-POLY", "KRW-SXP", "KRW-SRM", "KRW-STRK", "KRW-SBD", "KRW-IOTA", "KRW-ONT", "KRW-AAVE", "KRW-IOST", "KRW-HUNT", "KRW-PLA", "KRW-GLM", "KRW-XEC", "KRW-T", "KRW-AVAX", "KRW-ATOM", "KRW-POWR", "KRW-BAT", "KRW-ENJ", "KRW-ORBS", "KRW-LSK", "KRW-HIVE", "KRW-ICX", "KRW-OMG", "KRW-ELF", "KRW-THETA", "KRW-LINK", "KRW-TT", "KRW-CHZ", "KRW-AQT", "KRW-HBAR", "KRW-QTUM", "KRW-AERGO", "KRW-CRE", "KRW-STORJ", "KRW-DOT", "KRW-CELO", "KRW-NEO", "KRW-1INCH", "KRW-XLM", "KRW-MLK", "KRW-SC", "KRW-TON", "KRW-ANKR", "KRW-MVL", "KRW-CBK", "KRW-FCT2", "KRW-STMX", "KRW-ARDR", "KRW-BCH", "KRW-WAXP", "KRW-XTZ", "KRW-MED", "KRW-ARK", "KRW-TFUEL", "KRW-ONG", "KRW-STRAX", "KRW-LTC", "KRW-XEM", "KRW-META", "KRW-DKA", "KRW-UPP", "KRW-STPT", "KRW-RFR", "KRW-SNT", "KRW-MOC", "KRW-BTT", "KRW-GAS", "KRW-BTG", "KRW-SSX", "KRW-BSV", "KRW-AHT", "KRW-REP", "KRW-IQ", "KRW-LOOM", "KRW-CRO"]
list2 = ["DOGE", "BTC", "ETH", "STEEM", "TRX", "XRP", "KNC", "GMT", "NEAR", "NU", "BORA", "WAVES", "ZIL", "STX", "JST", "MTL", "AXS", "KAVA", "ZRX", "DAWN", "CVC", "SAND", "GRS", "WEMIX", "MBL", "EOS", "SOL", "PUNDIX", "ETC", "FLOW", "VET", "MATIC", "ADA", "ALGO", "HUM", "MFT", "MANA", "POLY", "SXP", "SRM", "STRK", "SBD", "IOTA", "ONT", "AAVE", "IOST", "HUNT", "PLA", "GLM", "XEC", "T", "AVAX", "ATOM", "POWR", "BAT", "ENJ", "ORBS", "LSK", "HIVE", "ICX", "OMG", "ELF", "THETA", "LINK", "TT", "CHZ", "AQT", "HBAR", "QTUM", "AERGO", "CRE", "STORJ", "DOT", "CELO", "NEO", "1INCH", "XLM", "MLK", "SC", "TON", "ANKR", "MVL", "CBK", "FCT2", "STMX", "ARDR", "BCH", "WAXP", "XTZ", "MED", "ARK", "TFUEL", "ONG", "STRAX", "LTC", "XEM", "META", "DKA", "UPP", "STPT", "RFR", "SNT", "MOC", "BTT", "GAS", "BTG", "SSX", "BSV", "AHT", "REP", "IQ", "LOOM", "CRO"]

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


def get_current_price(ticker, limit_info = True):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

def get_ror(k=0.5):
    df = pyupbit.get_ohlcv(list[i], count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'], 1)
    ror = df['ror'].cumprod()[-2]
    return ror
# 자동매매 시작
while True:
    try:
        for i in range(len(list)):
            temp_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            ror_max = 0.1
            for j in range(len(temp_list)):
                if get_ror(ror_max) < get_ror(temp_list[j]):
                    ror_max = temp_list[j]
            now = datetime.datetime.now()
            print(now)
            start_time = get_start_time(list[i])
            end_time = start_time + datetime.timedelta(days=1)
            if start_time < now < end_time - datetime.timedelta(seconds=10): #9시 ~ 8시 59분 50초면 True
                target_price = get_target_price(list[i], ror_max)    
                current_price = get_current_price(list[i])
                if target_price < current_price:
                    if current_price < target_price * 1.001 or current_price < target_price + 1 :
                        krw = get_balance("KRW")
                        if krw > 5000:
                            upbit.buy_market_order(list[i], krw*0.9995)
                if current_price > (target_price * 1.1):
                    btc = get_balance((list2[i]))
                    upbit.sell_market_order(list[i], btc*0.9995)

            else: # 8시 59분 50초 ~ 8시 59분 59초면 작동
                btc = get_balance(list2[i])
                if btc > 5000 / get_current_price(list[i]):
                    upbit.sell_market_order(list[i], btc*0.9995)
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)