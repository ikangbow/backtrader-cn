import backtrader as bt

from backtradercn.strategies.base import StrategyBase
import datetime as dt
import backtradercn.strategies.utils as bsu

class Basic5MA(StrategyBase):
    params = dict(
        maperiod_5=5,
        maperiod_10=10,
        maperiod_20=20,
        maperiod_30=30,
        maperiod_60=60,
        maperiod_stick = 8,
        maperiod_days = 4
    )

    def __init__(self):
        StrategyBase.__init__(self)
        self.ema_5 = bt.indicators.EMA(period=self.p.maperiod_5)
        self.ema_10 = bt.indicators.EMA(period=self.p.maperiod_10)
        self.ema_20 = bt.indicators.EMA(period=self.p.maperiod_20)
        self.ema_30 = bt.indicators.EMA(period=self.p.maperiod_30)
        self.ema_60 = bt.indicators.EMA(period=self.p.maperiod_60)
        self.rsi = bt.indicators.RelativeStrengthIndex()
        self.stick_n = 0
        self.profit = 0

    def update_indicators(self):
        self.profit = 0
        if self.buy_price and self.buy_price > 0:
            self.profit = float(self.data0.close[0] - self.buy_price) / self.buy_price
        self.max1 = max(self.ema_5, self.ema_10)
        self.max2 = max(self.max1, self.ema_20)
        self.max3 = max(self.max2, self.ema_30)
        self.max4 = max(self.max3, self.ema_60)
        self.min1 = min(self.ema_5, self.ema_10)
        self.min2 = min(self.min1, self.ema_20)
        self.min3 = min(self.min2, self.ema_30)
        self.min4 = min(self.min3, self.ema_60)
        # 粘合度
        self.stickness = (self.max4 - self.min4) / self.min4 * 100
        if self.stickness < self.p.maperiod_stick:
            self.stick_n += 1
        else:
            self.stick_n = 0

    def next(self):
        self.update_indicators()

        if self.order:  # waiting for pending order
            return

        if self.last_operation != "BUY":
            if self.ema_5 > self.ema_10 and self.ema_10 > self.ema_20 and self.ema_20 > self.ema_30 and self.ema_30 > self.ema_60 and self.stick_n > self.p.maperiod_days:
                self.long()
                self.buy_price = self.data0.close[0]
                if self.datas[0].datetime.date() == dt.datetime.now().date() - dt.timedelta(days=1):
                    stock_id = self.data._name
                    symbol = dt.datetime.now().strftime('%Y-%m-%d')
                    action = 'buy'
                    bsu.Utils.write_daily_alert(symbol, stock_id, action)

        if self.last_operation != "SELL":
            if self.ema_5 < self.ema_10 or self.profit < -0.02:
                self.short()
                self.reset_sell_indicators()
                if self.datas[0].datetime.date() == dt.datetime.now().date() - dt.timedelta(days=1):
                    stock_id = self.data._name
                    symbol = dt.datetime.now().strftime('%Y-%m-%d')
                    action = 'sell'
                    bsu.Utils.write_daily_alert(symbol, stock_id, action)