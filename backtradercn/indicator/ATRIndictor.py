import backtrader as bt
import talib


# 波动率
class ATRIndicator(bt.Indicator):
    lines = ('atr',)
    params = (('timeperiod', 14),)

    def __init__(self):
        self.lines.atr = bt.talib.ATR(self.data.high, self.data.low, self.data.close, timeperiod=14)
