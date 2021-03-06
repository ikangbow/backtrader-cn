# -*- coding: utf-8 -*-
import gevent.pool
import gevent.monkey
import tushare as ts
import backtradercn.datas.tushare as bdt
from backtradercn.libs.log import get_logger
from backtradercn.libs import models
from backtradercn.settings import settings as conf


gevent.monkey.patch_all()
logger = get_logger(__name__)


def download_delta_data(stocks, pool_size=40):
    """
    Download delta data for all stocks collections of all libraries.
    :param stocks: stock code list.
    :param pool_size: the pool size of gevent.pool.Pool.
    :return: None
    """

    pool = gevent.pool.Pool(pool_size)
    for i in range(len(stocks) // pool_size + 1):
        start = i * pool_size
        end = (i + 1) * pool_size
        lst = stocks[start:end]
        logger.debug(f'download delta data for stock list: {lst}')
        for stock in lst:
            pool.spawn(bdt.TsHisData.download_one_delta_data, stock)
        pool.join(timeout=30)


if __name__ == '__main__':
    # make sure the library exists
    models.get_or_create_library(conf.CN_STOCK_LIBNAME)

    hs300s = ts.get_hs300s()
    stock_pools = hs300s['code'].tolist() if 'code' in hs300s else []
    if not stock_pools:
        logger.warning('can not ts.geths300s() return empty.')
        stock_pools = models.get_cn_stocks()
    download_delta_data(stock_pools)
