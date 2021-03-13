import tushare as ts


if __name__ == '__main__':
    hs300s = ts.get_sme_classified()
    stock_pools = hs300s['code'].tolist() if 'code' in hs300s else []
    print(stock_pools)