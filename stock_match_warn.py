# -*- coding: utf-8 -*-
import time
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
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    msg = get_market_signal_by_date(date)
    print(msg)
    for stock_code in msg['buy']:
        # 经过测试，每隔3S进行一次买入操作的频率最合适
        time.sleep(3)
    else:
        logger.info("没有股票需要买入")


if __name__ == '__main__':
    print_Stock_Match()

