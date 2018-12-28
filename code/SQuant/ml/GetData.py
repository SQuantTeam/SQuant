# Author： 施源 Kris
# Create Time： 2018.8.15
import os
import numpy as np
import pandas as pd
import quandl  # 用quandl的api获取stock price 以苹果公司股票进行实验 代码-APPL
import tushare as ts
import datetime

print(ts.__version__)
ts.set_token('787e601c7738be1352a81c4aae6eae842a097e17f5d86514b3393cec')
# pro = ts.pro_api()

# df=pro.pro_bar( ts_code='000300.SH', adj='qfq', start_date='20180101', end_date='20181011')

# 上证综指，深证综指，沪深300
stock_index_list = ['000001.SH', '399106.SZ', '399300.SZ']

API_KEY = "gG8vr-_3fVigtYzrQf5B"  # 使用代码者需替换为自己的api_key
# my "fS5iVy_TsYAXGwAta2kN"
quandl.ApiConfig.api_key = API_KEY


def get_data(symbol, n_samples=500, save_to_csv=False):
    # 股票名称 —— 用户输入
    _symbol = symbol  # 默认为AAPL

    # 取最近N条数据 —— 用户输入
    _n_samples = n_samples  # 默认为3000

    # 拼凑用于请求的参数
    request_stock = 'WIKI/' + _symbol
    # print(request_stock)

    local_name = "{0}.csv".format(_symbol)

    # try:
    #     data = pd.read_csv(local_name)
    #     data = data[-n_samples:]
    #     return data
    # except OSError as e:
    #     print(e)

    # 列表出该目录下的所有文件(返回当前目录'.')
    for new_dir in os.listdir(os.curdir):
        # 如果有本地的数据就读取
        if new_dir.startswith(_symbol):
            data = pd.read_csv(local_name)
            data = data[-n_samples:]
            return data
        # 否则从Quandl请求数据
        else:
            try:
                data = quandl.Dataset(request_stock).data()
                # 转换为pandas的Dataframe形式
                df = data.to_pandas()
                # ---加上日期列，用于绘图
                df['Date'] = df.index
                # 保存数据到本地csv文件
                if save_to_csv:
                    data.to_csv(local_name, index=True)
                # 过老的数据没有太大的参考价值，取最近的n_samples条数据 
                _df = df[-n_samples:]
                return _df
            # 处理网络异常错误
            except IOError as e:
                print(e)
                return None

def get_stock(ts_code="000001.SZ", start_date='20180101',
              end_date=(datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y%m%d')):
    df = pd.DataFrame([])
    df = ts.pro_bar(pro_api=ts.pro_api(), ts_code=ts_code, adj='qfq', start_date=start_date, end_date=end_date)
    try:
        if df == None:
            df = ts.pro_bar(pro_api=ts.pro_api(), ts_code=ts_code, asset='I', start_date=start_date, end_date=end_date)
            df = df.sort_index(ascending=False)
    except:
        df = df.sort_index(ascending=True)
        print("get dataframe is not none,df.shape:", df.shape)
    # 设置成False能够按时间增序排列
    print("get_stock return:", df.shape)
    return df


def get_A_data(ts_code="000001.SZ", n_samples=500):
    yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y%m%d')
    df = get_stock(ts_code=ts_code, start_date="20100101", end_date=yesterday)
    df_n = df[-n_samples:]
    print("get_A_data shape:", df_n.shape)
    return df_n

    # df = ts.pro_bar(pro_api=ts.pro_api(), ts_code='399300.SZ', adj='qfq', start_date='20180101', end_date='20181225')
    # pro.daily(ts_code='399300.SZ', start_date='20180101', end_date='20181225')
    # 只有index_daily有效
    # df1 = pro.index_daily(ts_code='000300.SH', start_date='20180101', end_date='20181225')