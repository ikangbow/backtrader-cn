import backtrader as bt

from backtradercn.strategies.base import StrategyBase
from backtradercn.indicator import BreakIndicator as bi, MAIndicator as ma, ATRIndictor as at
import datetime as dt
import backtradercn.strategies.utils as bsu
from backtradercn.libs.log import get_logger

logger = get_logger(__name__)


class Basic5MA(StrategyBase):
    params = dict(
        maperiod_stick=8,
        maperiod_days=4
    )

    def __init__(self):
        StrategyBase.__init__(self)
        self.multiaverage = ma.MAIndicator(self.data)
        self.ema_5 = self.multiaverage.ma_5
        self.ema_10 = self.multiaverage.ma_10
        self.ema_20 = self.multiaverage.ma_20
        self.ema_30 = self.multiaverage.ma_30
        self.ema_60 = self.multiaverage.ma_60
        # rsi
        self.rsi = bt.indicators.RelativeStrengthIndex()
        self.rsi.plotinfo.plot = False
        # 唐安奇通道
        self.upAndDown = bi.BreakIndicator(self.data)
        self.buysig = bt.indicators.CrossOver(self.datas[0].close, self.upAndDown.up)
        self.sellsig = bt.indicators.CrossDown(self.datas[0].close, self.upAndDown.down)
        # 图上显示上下轨
        self.upAndDown.plotinfo.plotmaster = self.data
        # 图上不显示买卖信号
        self.buysig.plotinfo.plot = False
        self.sellsig.plotinfo.plot = False
        # 主图上显示均线
        self.multiaverage.plotinfo.plotmaster = self.data
        # 波动率指标
        self.atr = at.ATRIndicator(self.data)
        self.atr.plotinfo.plotmaster = self.data
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
            if self.ema_5[0] > self.ema_10[0] and self.ema_10[0] > self.ema_20[0] and self.ema_20[0] > self.ema_30[
                0] and self.ema_30[0] > self.ema_60[0] and self.buysig[0] == 1 and self.data0.close[0] > (self.data0.close[-1]+ self.atr[0]):
                self.long()
                self.buy_price = self.data0.close[0]
                if self.datas[0].datetime.date() == dt.datetime.now().date() - dt.timedelta(days=1):
                    stock_id = self.data._name
                    symbol = dt.datetime.now().strftime('%Y-%m-%d')
                    action = 'buy'
                    bsu.Utils.write_daily_alert(symbol, stock_id, action)

        if self.last_operation != "SELL":
            if (self.ema_5[0] < self.ema_10[0] and self.profit >= 0.05) or self.profit < -0.03:
                self.short()
                if self.datas[0].datetime.date() == dt.datetime.now().date() - dt.timedelta(days=1):
                    stock_id = self.data._name
                    symbol = dt.datetime.now().strftime('%Y-%m-%d')
                    action = 'sell'
                    bsu.Utils.write_daily_alert(symbol, stock_id, action)
