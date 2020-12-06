# -*- coding: utf-8 -*-
import os
import pandas as pd
from datetime import datetime, timedelta
from backtradercn.libs.models import get_library
from backtradercn.settings import settings as conf
from backtradercn.libs.log import get_logger

logger = get_logger(__name__)

def get_market_signal_by_date(date):
    msg = {
        'buy': [],
        'sell': [],
    }

    lib = get_library(conf.DAILY_STOCK_ALERT_LIBNAME)
    if lib:
        if date in lib.list_symbols():
            data = lib.read(date).data
            data = data.to_dict('records')
            for item in data:
                if item['action'] == 'buy':
                    msg['buy'].append(item['stock'])
                elif item['action'] == 'sell':
                    msg['sell'].append(item['stock'])

    return msg

def print_Stock_Match():
    RESULT_PATH = os.path.join(
        conf.RESULT_DIR,
        f'{datetime.now().strftime("%Y%m%d-%H%M%S-%f")}.csv'
    )
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    msg = get_market_signal_by_date(date)
    stocks = []
    for stock_code in msg['buy']:
        # 经过测试，每隔3S进行一次买入操作的频率最合适
        stocks.append(str(stock_code).zfill(6))
    else:
        logger.info("没有股票需要买入")

    name=['code']
    cn_stocks = pd.DataFrame(columns=name, data=stocks)
    cn_stocks.to_csv(RESULT_PATH, index=False,encoding='utf_8_sig')

if __name__ == '__main__':
    print_Stock_Match()

