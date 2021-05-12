import pyupbit
import time
import datetime

access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)

def cal_target(ticker):
    df = pyupbit.get_ohlcv(ticker, "day", 2)
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    cal_target = today['open'] + yesterday_range * 0.5
    return cal_target

def vol_target(ticker):
    df = pyupbit.get_ohlcv(ticker, "day", 2)
    yesterday = df.iloc[-2]
    vol_target = 0.04 / ((yesterday['high'] - yesterday['low']) / yesterday['close'])
    if vol_target < 1:
        return vol_target
    else:
        return 1

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker, "day", 6)
    close = df['close']
    ma5 = close.rolling(5).mean()
    return ma5[-2]

def get_ma_score (ticker):
    current_price = pyupbit.get_current_price(ticker)
    df = pyupbit.get_ohlcv(ticker, "day", 21)
    df['ma3'] = df['close'].rolling(window=3).mean()
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['ma15'] = df['close'].rolling(window=15).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    if current_price >= df['ma3'][-2]:
        ma3_score = 0.2
    else:
        ma3_score = 0
    if current_price >= df['ma5'][-2]:
        ma5_score = 0.2
    else:
        ma5_score = 0
    if current_price >= df['ma10'][-2]:
        ma10_score = 0.2
    else:
        ma10_score = 0
    if current_price >= df['ma15'][-2]:
        ma15_score = 0.2
    else:
        ma15_score = 0
    if current_price >= df['ma20'][-2]:
        ma20_score = 0.2
    else:
        ma20_score = 0
    ma_score = ma3_score + ma5_score + ma10_score + ma15_score + ma20_score
    return ma_score

op_mode_BTC = False
hold_BTC = False
op_mode_ETH = False
hold_ETH = False
op_mode_XRP = False
hold_XRP = False
op_mode_BCH = False
hold_BCH = False
op_mode_EOS = False
hold_EOS = False

while True:
    try:
        now = datetime.datetime.now()

        if now.hour == 8 and now.minute == 59 and (50 <= now.second <= 59):
            # BTC
            if op_mode_BTC is True and hold_BTC is True:
                BTC_balance = upbit.get_balance("KRW-BTC")
                upbit.sell_market_order("KRW-BTC", BTC_balance)
                op_mode_BTC = False
                hold_BTC = False
            # ETH
            if op_mode_ETH is True and hold_ETH is True:
                ETH_balance = upbit.get_balance("KRW-ETH")
                upbit.sell_market_order("KRW-ETH", ETH_balance)
                op_mode_ETH = False
                hold_ETH = False
            # XRP
            if op_mode_XRP is True and hold_XRP is True:
                XRP_balance = upbit.get_balance("KRW-XRP")
                upbit.sell_market_order("KRW-XRP", XRP_balance)
                op_mode_XRP = False
                hold_XRP = False
            # BCH
            if op_mode_BCH is True and hold_BCH is True:
                BCH_balance = upbit.get_balance("KRW-BCH")
                upbit.sell_market_order("KRW-BCH", BCH_balance)
                op_mode_BCH = False
                hold_BCH = False
            # EOS
            if op_mode_EOS is True and hold_EOS is True:
                EOS_balance = upbit.get_balance("KRW-EOS")
                upbit.sell_market_order("KRW-EOS", EOS_balance)
                op_mode_EOS = False
                hold_EOS = False

        if now.hour == 9 and now.minute == 0 and (20 <= now.second <= 30):
            krw_balance = upbit.get_balance("KRW")
            # BTC
            target_BTC = cal_target("KRW-BTC")
            vol_BTC = vol_target("KRW-BTC")
            ma5_BTC = get_yesterday_ma5("KRW-BTC")
            op_mode_BTC = True
            # ETH
            target_ETH = cal_target("KRW-ETH")
            vol_ETH = vol_target("KRW-ETH")
            ma5_ETH = get_yesterday_ma5("KRW-ETH")
            op_mode_ETH = True
            # XRP
            target_XRP = cal_target("KRW-XRP")
            vol_XRP = vol_target("KRW-XRP")
            ma5_XRP = get_yesterday_ma5("KRW-XRP")
            op_mode_XRP = True
            time.sleep(1)
            # BCH
            target_BCH = cal_target("KRW-BCH")
            vol_BCH = vol_target("KRW-BCH")
            ma5_BCH = get_yesterday_ma5("KRW-BCH")
            op_mode_BCH = True
            # EOS
            target_EOS = cal_target("KRW-EOS")
            vol_EOS = vol_target("KRW-EOS")
            ma5_EOS = get_yesterday_ma5("KRW-EOS")
            op_mode_EOS = True
            time.sleep(1)

        price_BTC = pyupbit.get_current_price("KRW-BTC")
        price_ETH = pyupbit.get_current_price("KRW-ETH")
        price_XRP = pyupbit.get_current_price("KRW-XRP")
        price_BCH = pyupbit.get_current_price("KRW-BCH")
        price_EOS = pyupbit.get_current_price("KRW-EOS")

        # BTC
        if op_mode_BTC is True and hold_BTC is False and price_BTC is not None and price_BTC >= target_BTC and price_BTC >= ma5_BTC:
            ma_score_BTC = get_ma_score("KRW-BTC")
            upbit.buy_market_order("KRW-BTC", krw_balance * 0.2 * vol_BTC * ma_score_BTC)
            hold_BTC = True
        # ETH
        if op_mode_ETH is True and hold_ETH is False and price_ETH is not None and price_ETH >= target_ETH and price_ETH >= ma5_ETH:
            ma_score_ETH = get_ma_score("KRW-ETH")
            upbit.buy_market_order("KRW-ETH", krw_balance * 0.2 * vol_ETH * ma_score_ETH)
            hold_ETH = True
        # XRP
        if op_mode_XRP is True and hold_XRP is False and price_XRP is not None and price_XRP >= target_XRP and price_XRP >= ma5_XRP:
            ma_score_XRP = get_ma_score("KRW-XRP")
            upbit.buy_market_order("KRW-XRP", krw_balance * 0.2 * vol_XRP * ma_score_XRP)
            hold_XRP = True
        # BCH
        if op_mode_BCH is True and hold_BCH is False and price_BCH is not None and price_BCH >= target_BCH and price_BCH >= ma5_BCH:
            ma_score_BCH = get_ma_score("KRW-BCH")
            upbit.buy_market_order("KRW-BCH", krw_balance * 0.2 * vol_BCH * ma_score_BCH)
            hold_BCH = True
        # EOS
        if op_mode_EOS is True and hold_EOS is False and price_EOS is not None and price_EOS >= target_EOS and price_EOS >= ma5_EOS:
            ma_score_EOS = get_ma_score("KRW-EOS")
            upbit.buy_market_order("KRW-EOS", krw_balance * 0.2 * vol_EOS * ma_score_EOS)
            hold_EOS = True

    except Exception as e:
        print(e)

    time.sleep(1)