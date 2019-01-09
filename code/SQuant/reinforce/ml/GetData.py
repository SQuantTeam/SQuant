
# -*- coding: UTF-8 -*-
# Create Time： 2018.8.15
import os
import sys
import numpy as np
import pandas as pd
import quandl  # 用quandl的api获取stock price 以苹果公司股票进行实验 代码-APPL
import tushare as ts
import datetime

sys.path.append("../..")
from trader.sqSetting import MdAddress, TdAddress, DefaultPhone, DefaultToken
from trader.gateway.tradeGateway import TradeGateway

# from trader.sqConstant import *
# from trader.sqGateway import *
# from trader.trade.riskManager import RiskManager

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


def get_stock(ts_code="000001.SZ", start_date='20100101',
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


def get_A_data(ts_code="000001.SZ", end_date=(datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y%m%d'),
               n_samples=1000):
    print("end_date:", end_date)
    # yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y%m%d')
    df = get_stock(ts_code=ts_code, start_date="20090101", end_date=end_date)
    print("get_A_data df.iloc[-1]:", df.iloc[-1])
    df_n = df[-n_samples:]
    print("get_A_data shape:", df_n.shape)
    print("get_A_data df_n.iloc[-1]:", df_n.iloc[-1])
    return df_n


def get_latest_bar(symbol, trade_date, freq):
    # phone = request.session.get('phone', None)
    # token = request.session.get('token', None)
    print("exec GetData->get_latest_bar method")
    phone = DefaultPhone
    token = DefaultToken
    setting = {}
    setting['mdAddress'] = MdAddress
    setting['tdAddress'] = TdAddress
    setting['username'] = phone
    setting['token'] = token
    tradeGateway = TradeGateway(setting, gatewayName="SQuant")
    if tradeGateway.loginStatus == False:
        print("GetData->get_latest_bar:loginStatus==False")
        return None
    else:
        if not cmp(freq, "5M") and not cmp(freq, "1M"):
            freq = "5M"
        if trade_date.__len__() == 8:
            trade_date = (trade_date[0:4] + "-" + trade_date[4:6] + "-" + trade_date[6:8])
        print("tradedate:", trade_date)
        df, msg = tradeGateway.qryQuoteBar(symbol=symbol, trade_date=trade_date, freq=freq)
        # 释放资源
        tradeGateway.close()
        print("msg:", msg)
        if df is None:
            print("GetData->get_latest_bar:get data none")
            return None
        print(df.shape, type(df))
        df['close'] = df['low'] * 1.05
        # result = df.to_json(orient='records')
        # print("GetData->get_latest_bar:df  [", result)
        return df


# df = ts.pro_bar(pro_api=ts.pro_api(), ts_code='399300.SZ', adj='qfq', start_date='20180101', end_date='20181225')
# pro.daily(ts_code='399300.SZ', start_date='20180101', end_date='20181225')
# 只有index_daily有效
# df1 = pro.index_daily(ts_code='000300.SH', start_date='20180101', end_date='20181225')

if __name__ == '__main__':
    get_latest_bar(symbol="000001.SH", trade_date="2019-01-09", freq="1M")
