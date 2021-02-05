# -*- coding: utf-8 -*-
import backtrader as bt

class StrategyBase(bt.Strategy):
    def __init__(self):
        self.order = None
        self.last_operation = "SELL"
        self.status = "DISCONNECTED"
        self.bar_executed = 0
        self.buy_price_close = None
        self.soft_sell = False
        self.hard_sell = False

    def reset_sell_indicators(self):
        self.soft_sell = False
        self.hard_sell = False
        self.buy_price_close = None

    def notify_data(self, data, status, *args, **kwargs):
        self.status = data._getstatusname(status)

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

                print(order.__dict__)

            else:  # Sell
                self.last_operation = "SELL"
                self.reset_sell_indicators()
            # Sentinel to None: new orders allowed
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            pass
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        color = 'green'
        if trade.pnl < 0:
            color = 'red'
