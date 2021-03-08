# -*- coding: utf-8 -*-
import os

PROJECT_NAME = 'backtradercn'

'''***获取上上级目录***'''
rootPath = os.path.abspath(os.path.join(os.getcwd(), "../.."))
# log setting
LOG_DIR = os.path.join(rootPath,'log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
DEBUG = True

# database setting
MONGO_HOST = 'localhost'
CN_STOCK_LIBNAME = 'ts_his_lib'
DAILY_STOCK_ALERT_LIBNAME = 'daily_stock_alert'
STRATEGY_PARAMS_LIBNAME = 'strategy_params'
STRATEGY_PARAMS_MA_SYMBOL = 'ma_trend'

# 1、home目录下建立log文件夹以及data/mongodb/log文件夹  全部可编辑
# 2、rootPath = os.path.abspath(os.path.join(os.getcwd(), "../"))

