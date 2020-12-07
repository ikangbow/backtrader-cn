# -*- coding: utf-8 -*-

import backtradercn.datas.tushare as bdt
from backtradercn.libs.log import get_logger

logger = get_logger(__name__)

class QA_Fetch_Data():
    @classmethod
    def get_data(cls, coll_name):
        """
        Get the time serials used by strategy.
        :param coll_name: stock id (string).
        :return: time serials(DataFrame).
        """
        ts_his_data = bdt.TsHisData(coll_name)

        return ts_his_data.get_data()

if __name__ == '__main__':
    df = QA_Fetch_Data.get_data('600025');
    print('---------获取某月的数据-----------')
    data = df['2020-11-11':'2020-12-04']  # 获取时间区间的值
    print(data)