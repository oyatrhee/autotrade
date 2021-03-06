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
    vol_target = 0.03 / ((yesterday['high'] - yesterday['low']) / yesterday['close'])
    if vol_target < 1:
        return vol_target
    else:
        return 1

def get_ma_score (ticker):
    current_price = pyupbit.get_current_price(ticker)
    df = pyupbit.get_ohlcv(ticker, "day", 20)
    df['ma3'] = df['close'].rolling(window=3).mean()
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['ma15'] = df['close'].rolling(window=15).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    if current_price >= df['ma3'][-1]:
        ma3_score = 0.2
    else:
        ma3_score = 0
    if current_price >= df['ma5'][-1]:
        ma5_score = 0.2
    else:
        ma5_score = 0
    if current_price >= df['ma10'][-1]:
        ma10_score = 0.2
    else:
        ma10_score = 0
    if current_price >= df['ma15'][-1]:
        ma15_score = 0.2
    else:
        ma15_score = 0
    if current_price >= df['ma20'][-1]:
        ma20_score = 0.2
    else:
        ma20_score = 0
    ma_score = ma3_score + ma5_score + ma10_score + ma15_score + ma20_score
    return ma_score

op_mode_BTC = False
hold_BTC = False
op_mode_ETH = False
hold_ETH = False
op_mode_ADA = False
hold_ADA = False
op_mode_BCH = False
hold_BCH = False
op_mode_SOL = False
hold_SOL = False

while True:
    try:
        now = datetime.datetime.now()

        if now.hour == 8 and now.minute == 59 and (55 <= now.second <= 59):
            # BTC
            if op_mode_BTC is True and hold_BTC is True:
                BTC_balance = upbit.get_balance("KRW-BTC")
                if BTC_balance > 0:
                    upbit.sell_market_order("KRW-BTC", BTC_balance)
                    op_mode_BTC = False
                    hold_BTC = False
                else:
                    op_mode_BTC = False
                    hold_BTC = False

            # ETH
            if op_mode_ETH is True and hold_ETH is True:
                ETH_balance = upbit.get_balance("KRW-ETH")
                if ETH_balance > 0:
                    upbit.sell_market_order("KRW-ETH", ETH_balance)
                    op_mode_ETH = False
                    hold_ETH = False
                else:
                    op_mode_ETH = False
                    hold_ETH = False
            # ADA
            if op_mode_ADA is True and hold_ADA is True:
                ADA_balance = upbit.get_balance("KRW-ADA")
                if ADA_balance > 0:
                    upbit.sell_market_order("KRW-ADA", ADA_balance)
                    op_mode_ADA = False
                    hold_ADA = False
                else:
                    op_mode_ADA = False
                    hold_ADA = False
            # BCH
            if op_mode_BCH is True and hold_BCH is True:
                BCH_balance = upbit.get_balance("KRW-BCH")
                if BCH_balance > 0:
                    upbit.sell_market_order("KRW-BCH", BCH_balance)
                    op_mode_BCH = False
                    hold_BCH = False
                else:
                    op_mode_BCH = False
                    hold_BCH = False
            # SOL
            if op_mode_SOL is True and hold_SOL is True:
                SOL_balance = upbit.get_balance("KRW-SOL")
                if SOL_balance > 0:
                    upbit.sell_market_order("KRW-SOL", SOL_balance)
                    op_mode_SOL = False
                    hold_SOL = False
                else:
                    op_mode_SOL = False
                    hold_SOL = False

        if now.hour == 9 and now.minute == 0 and (20 <= now.second <= 25):
            krw_balance = upbit.get_balance("KRW")
            # BTC
            target_BTC = cal_target("KRW-BTC")
            vol_BTC = vol_target("KRW-BTC")
            op_mode_BTC = True
            # ETH
            target_ETH = cal_target("KRW-ETH")
            vol_ETH = vol_target("KRW-ETH")
            op_mode_ETH = True
            # ADA
            target_ADA = cal_target("KRW-ADA")
            vol_ADA = vol_target("KRW-ADA")
            op_mode_ADA = True
            # BCH
            target_BCH = cal_target("KRW-BCH")
            vol_BCH = vol_target("KRW-BCH")
            op_mode_BCH = True
            # SOL
            target_SOL = cal_target("KRW-SOL")
            vol_SOL = vol_target("KRW-SOL")
            op_mode_SOL = True
            time.sleep(1)

        price_BTC = pyupbit.get_current_price("KRW-BTC")
        price_ETH = pyupbit.get_current_price("KRW-ETH")
        price_ADA = pyupbit.get_current_price("KRW-ADA")
        price_BCH = pyupbit.get_current_price("KRW-BCH")
        price_SOL = pyupbit.get_current_price("KRW-SOL")

        # BTC
        if op_mode_BTC is True and hold_BTC is False and price_BTC >= target_BTC:
            ma_score_BTC = get_ma_score("KRW-BTC")
            current_krw = upbit.get_balance("KRW")
            position_BTC = krw_balance * 0.2 * vol_BTC * ma_score_BTC
            if 5000 < position_BTC < current_krw:
                upbit.buy_market_order("KRW-BTC", position_BTC)
                hold_BTC = True
            else:
                op_mode_BTC = False
        # ETH
        if op_mode_ETH is True and hold_ETH is False and price_ETH >= target_ETH:
            ma_score_ETH = get_ma_score("KRW-ETH")
            current_krw = upbit.get_balance("KRW")
            position_ETH = krw_balance * 0.2 * vol_ETH * ma_score_ETH
            if 5000 < position_ETH < current_krw:
                upbit.buy_market_order("KRW-ETH", position_ETH)
                hold_ETH = True
            else:
                op_mode_ETH = False
        # ADA
        if op_mode_ADA is True and hold_ADA is False and price_ADA >= target_ADA:
            ma_score_ADA = get_ma_score("KRW-ADA")
            current_krw = upbit.get_balance("KRW")
            position_ADA = krw_balance * 0.2 * vol_ADA * ma_score_ADA
            if 5000 < position_ADA < current_krw:
                upbit.buy_market_order("KRW-ADA", position_ADA)
                hold_ADA = True
            else:
                op_mode_ADA = False
        # BCH
        if op_mode_BCH is True and hold_BCH is False and price_BCH >= target_BCH:
            ma_score_BCH = get_ma_score("KRW-BCH")
            current_krw = upbit.get_balance("KRW")
            position_BCH = krw_balance * 0.2 * vol_BCH * ma_score_BCH
            if 5000 < position_BCH < current_krw:
                upbit.buy_market_order("KRW-BCH", position_BCH)
                hold_BCH = True
            else:
                op_mode_BCH = False
        # SOL
        if op_mode_SOL is True and hold_SOL is False and price_SOL >= target_SOL:
            ma_score_SOL = get_ma_score("KRW-SOL")
            current_krw = upbit.get_balance("KRW")
            position_SOL = krw_balance * 0.2 * vol_SOL * ma_score_SOL
            if 5000 < position_SOL < current_krw:
                upbit.buy_market_order("KRW-SOL", position_SOL)
                hold_SOL = True
            else:
                op_mode_SOL = False

    except Exception as e:
        print(e)

    time.sleep(1)
