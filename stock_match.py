# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from daily_alert import get_market_signal_by_date
from backtradercn.libs.log import get_logger
from backtradercn.libs.Mail import *
import json

logger = get_logger(__name__)


def update__stock_match():
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    msg = get_market_signal_by_date(date)
    buy_msg = ''
    sell_msg=''
    mm = ''
    if len(msg['buy']) == 0:
        pass
    else:
        buy_msg = ','.join(msg['buy'])
    if len(msg['sell']) == 0:
        pass
    else:
        sell_msg = ','.join(msg['sell'])

    if len(buy_msg)==0:
        pass
    else:
        mm += '建议买入:' + buy_msg
    if len(sell_msg)==0:
        pass
    else:
        mm += ',建议卖出:' + sell_msg
    if len(mm)==0 :
        pass
    else:
       Mail().sendMail(mm,date, "1078162876@qq.com")

if __name__ == '__main__':
    update__stock_match()
