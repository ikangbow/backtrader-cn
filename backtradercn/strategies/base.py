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
        self.buy_price = None
        logger.debug('>>Starting strategy...')

    def reset_sell_indicators(self):
        self.buy_price_ = None

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
                              'Stock %s buy Executed, portfolio value is %.2f' %
                              (self.data._name,
                               self.broker.get_value()))

            else:  # Sell
                self.last_operation = "SELL"
                self.reset_sell_indicators()
                bsu.Utils.log(self.datas[0].datetime.date(),
                              'Stock %s sell Executed, portfolio value is %.2f' %
                              (self.data._name,
                               self.broker.get_value()))
            # Sentinel to None: new orders allowed
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            bsu.Utils.log(self.datas[0].datetime.date(),
                          'order Canceled/Margin/Rejected, order_status is %d',
                           order.status)
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        bsu.Utils.log(self.datas[0].datetime.date(), 'Stock %s,策略收益毛收益:%.2f,净收益:%.2f' %
        (self.data._name,trade.pnl,trade.pnlcomm))

    def stop(self):
        bsu.Utils.log(self.datas[0].datetime.date(), '期末总资金:%.2f' %(self.broker.get_value()))
