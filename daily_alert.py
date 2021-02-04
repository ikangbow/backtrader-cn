import datetime as dt
import json

from backtradercn.libs.log import get_logger
from backtradercn.settings import settings as conf
from backtradercn.libs.models import get_library
from backtradercn.libs.Mail import *

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


def send_daily_alert():
    date = dt.datetime.now().strftime('%Y-%m-%d')
    msg = get_market_signal_by_date(date)
    Mail().sendMail(date, json.dumps(msg), "1078162876@qq.com")



if __name__ == '__main__':
    send_daily_alert()
