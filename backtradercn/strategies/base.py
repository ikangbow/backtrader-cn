# -*- coding: utf-8 -*-
import backtrader as bt
from backtradercn.libs.log import get_logger
import backtradercn.strategies.utils as bsu

logger = get_logger(__name__)

class StrategyBase(bt.Strategy):
    def __init__(self):
        self.order = None
        self.last_operation = "SELL"
        self.bar_executed = 0
        self.buy_price_close = None
        logger.debug('>>Starting strategy...')

    def reset_sell_indicators(self):
        self.buy_price_close = None

    def short(self):
        if self.last_operation == "SELL":
            return
        return self.sell()

    def long(self):
        if self.last_operation == "BUY":
            return
        return self.buy()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED', True)

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.last_operation = "BUY"
                bsu.Utils.log(self.datas[0].datetime.date(),
                              f'买入==>价格:{order.executed.price},成本==>{order.executed.value:.2f},手续费==>{order.executed.comm:.2f}')

            else:  # Sell
                self.last_operation = "SELL"
                self.reset_sell_indicators()
                bsu.Utils.log(self.datas[0].datetime.date(),
                              f'卖出==>价格:{order.executed.price},成本==>{order.executed.value:.2f},手续费==>{order.executed.comm:.2f}')
            # Sentinel to None: new orders allowed
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            bsu.Utils.log(self.datas[0].datetime.date(),
                          'order Canceled/Margin/Rejected, order_status is %d',
                           order.status)
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        bsu.Utils.log(self.datas[0].datetime.date(),f'策略收益：毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')
