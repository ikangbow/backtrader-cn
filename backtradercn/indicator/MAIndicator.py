import backtrader as bt
import backtrader.indicators as btind

# 多头均线发散向上
class MAIndicator(bt.Indicator):
    lines = ('ma_5', 'ma_10', 'ma_20', 'ma_30', 'ma_60')
    params = (('maperiod_5', 5), ('maperiod_10', 10), ('maperiod_20', 20), ('maperiod_30', 30), ('maperiod_60', 60))

    def __init__(self):
        close = self.data.close
        self.lines.ma_5 = btind.EMA(self.data, period=self.p.maperiod_5)
        self.lines.ma_10 = btind.EMA(self.data, period=self.p.maperiod_10)
        self.lines.ma_20 = btind.EMA(self.data, period=self.p.maperiod_20)
        self.lines.ma_30 = btind.EMA(self.data, period=self.p.maperiod_30)
        self.lines.ma_60 = btind.EMA(self.data, period=self.p.maperiod_60)
