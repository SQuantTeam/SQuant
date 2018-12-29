# -*- coding: UTF-8 -*-
import os
import numpy as np
import pandas as pd
import quandl  # 用quandl的api获取stock price 以苹果公司股票进行实验 代码-APPL

API_KEY = "gG8vr-_3fVigtYzrQf5B" # 使用代码者需替换为自己的api_key
quandl.ApiConfig.api_key = API_KEY


def get_data(symbol, n_samples = 500, save_to_csv=False):

    # 股票名称 —— 用户输入
    _symbol = symbol #默认为AAPL

    # 取最近N条数据 —— 用户输入
    _n_samples = n_samples #默认为3000

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

    #列表出该目录下的所有文件(返回当前目录'.')
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
                # 保存数据到本地csv文件
                if save_to_csv:
                    data.to_csv(local_name)
                # 过老的数据没有太大的参考价值，取最近的n_samples条数据 
                _df = df[-n_samples:]
                return _df
            # 处理网络异常错误
            except IOError as e:
                print(e)
                return None
        