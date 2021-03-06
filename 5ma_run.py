import backtrader as bt
import multiprocessing
import backtradercn.analyzers.drawdown as bad
import backtradercn.strategies.utils as bsu
import backtradercn.datas.tushare as bdt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
from backtradercn.strategies.basic_ma import Basic5MA
from backtradercn.settings import settings as conf
from backtradercn.libs import models


class MA5:
    @classmethod
    def get_data(cls, coll_name):
        """
        Get the time serials used by strategy.
        :param coll_name: stock id (string).
        :return: time serials(DataFrame).
        """
        ts_his_data = bdt.TsHisData(coll_name)

        return ts_his_data.get_data()

    def run_back_testing(cls, stock_id):
        """
        Run the back testing, return the analysis data.
        :param stock_id(string)
        :return(dict): analysis data.
        """
        # get the data
        data = cls.get_data(stock_id)
        cerebro = bt.Cerebro()
        data = bt.feeds.PandasData(dataname=data)
        cerebro.adddata(data, name=stock_id)
        cerebro.addstrategy(Basic5MA)
        cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='al_return',
                            timeframe=bt.analyzers.TimeFrame.NoTimeFrame)

        cerebro.addanalyzer(bad.TimeDrawDown, _name='al_max_drawdown')

        cerebro.broker.set_cash(bsu.Utils.DEFAULT_CASH)

        cerebro.addsizer(bt.sizers.FixedSize, stake=100)

        cerebro.broker.setcommission(commission=0.005)

        cerebro.run()
        if conf.DEBUG:
            list = [stock_id, '.html']
            b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo(), filename=''.join(list), output_mode='show')
            cerebro.plot(b)

    def main(cls, stock_pools):
        """
        Get all stocks and run back test.
        :param stock_pools: list, the stock code list.
        :return: None
        """

        pool = multiprocessing.Pool()
        for stock in stock_pools:
            pool.apply_async(MA5().run_back_testing, args=(stock,))
        pool.close()
        pool.join()


if __name__ == '__main__':
    MA5().run_back_testing("601857")
    #cn_stocks = models.get_cn_stocks()
    #MA5().main(cn_stocks)
