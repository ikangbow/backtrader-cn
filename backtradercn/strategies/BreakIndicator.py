# 平台突破指标
import backtrader as bt

class BreakIndicator(bt.Indicator):
    # 定义上轨,下轨 3根线的上下轨
    lines = ("up","down")
    params = (
        ('maperiod', 5),
    )
    def __init__(self):
        self.addminperiod(self.params.maperiod+1)

    def next(self):
        self.up[0] = max(self.datas[0].high.get(ago = -1,size=self.params.maperiod))
        self.down[0] = min(self.datas[0].low.get(ago = -1,size=self.params.maperiod))