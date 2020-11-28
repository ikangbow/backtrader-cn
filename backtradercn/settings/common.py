# -*- coding: utf-8 -*-
import os
import sys

PROJECT_NAME = 'backtradercn'
rootPath = os.path.dirname(os.path.abspath(sys.argv[0]))
# log setting
LOG_DIR = os.path.join(rootPath,'temp')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

# database setting
MONGO_HOST = 'localhost'
CN_STOCK_LIBNAME = 'ts_his_lib'
DAILY_STOCK_ALERT_LIBNAME = 'daily_stock_alert'
STRATEGY_PARAMS_LIBNAME = 'strategy_params'
STRATEGY_PARAMS_MA_SYMBOL = 'ma_trend'

# wechat
WECHAT_APP_ID = 'wx5e8e3c4779887f32'
WECHAT_APP_SECRET = 'd4624c36b6795d1d99dcf0547af5443d'

# xueqiu account
XQ_ACCOUNT = os.getenv('XQ_ACCOUNT', '18210563565')
XQ_PASSWORD = os.getenv('XQ_PASSWORD', 'kbw248655')
XQ_PORTFOLIO_MARKET = os.getenv('XQ_PORTFOLIO_MARKET', 'cn')
# 默认的组合前缀，组合名称格式为 组合前缀 + 股票代码
# 组合名字
XQ_CUBES_PREFIX = 'SC'
# 默认创建组合时股票的初始百分数
XQ_DEFAULT_BUY_WEIGHT = 5

SINA_CONFIG = {
    "username": os.getenv('WEIBO_USERNAME', '18210563565'),
    "password": os.getenv('WEIBO_PASSWORD', 'kbw248655'),
    "request_headers": {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'no-cache',
        'Referer': 'http://jiaoyi.sina.com.cn/jy/index.php',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    },
    "login_url": "https://login.sina.com.cn/sso/login.php",
}
