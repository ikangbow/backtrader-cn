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
    json_str = json.dumps(msg)
    print(json_str)
    Mail().sendMail(date,json.dumps(msg), "1078162876@qq.com")


if __name__ == '__main__':
    update__stock_match()
