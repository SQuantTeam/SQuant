# Author： 施源 Kris
# Create Time： 2018.8.15

import numpy as np
import pandas as pd


def data_preprocess(data, split_ratio):
    """
    :param data:
    :param split_ratio: 训练集的比例大小
    :return:
    """
    _data = data
    _split_ratio = split_ratio

    # 数据行数
    n_rows = _data.shape[0]
    # 数据列数
    n_cols = _data.shape[1]
    # 获取开盘价数据列
    data_c_open = _data[['Open']]
    # 错开一位，取后一天的开盘价
    tradePrice = np.array(data_c_open[1:])
    # 其余列少取一天的数据
    _data = _data[:-1]
    # 若两者行数相等，则可以拼接数据
    if len(tradePrice) == len(_data):
        # 取历史的开盘价、收盘价、最低价、最高价、成交量
        _data = _data.loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']]
        # 用后一天，也即当天的开盘价，作为交易价格
        _data['tradePrice'] = tradePrice
        # 初始化现金为100000. (默认初始资本为10w)
        _data['cash'] = 100000.
        # 初始化股票价值为0（默认当前未持股）
        _data['stockValue'] = 0.
        date_series = data['Date']
        # _data['Date']= data.loc[:,['Date']]
        # 将处理后的数据转换为numpy数组
        _data = np.array(_data)

        # 训练数据条数
        n_train = int(np.round(_split_ratio * n_rows))
        # 测试数据条数
        n_test = n_rows - n_train

        # 训练数据集
        train = _data[:n_train]
        date_train = date_series[:n_train]
        # 测试数据集
        test = _data[-n_test:]
        date_test = date_series[-n_test:]
        return train, test, date_train, date_test

    else:
        return None, None


def data_A_preprocess(data, split_ratio):
    """
     :param data:
     :param split_ratio: 训练集的比例大小
     :return:
     """
    _data = data
    _split_ratio = split_ratio

    # 数据行数
    n_rows = _data.shape[0]
    # 数据列数
    n_cols = _data.shape[1]
    # # 获取开盘价数据列
    data_c_open = _data[['open']]

    # # 若两者行数相等，则可以拼接数据
    # if len(tradePrice) == len(_data):
    # 取历史的开盘价、收盘价、最低价、最高价、成交量
    # ts_code，trade_date，open，high，low，close，pre_close，change，pct_change，vol，amount
    # ['Open', 'High', 'Low', 'Close', 'Volume']
    # 'pre_close', 'change', 'pct_change', 'amount'
    _data = _data.loc[:, ['open', 'high', 'low', 'close', 'vol']]
    # 用当天的最高价与最低价的平均值进行
    _data['tradePrice'] = (_data['high'] + _data['low']) / 2.0

    # 初始化现金为100000. (默认初始资本为10w)
    _data['cash'] = 100000.
    # 初始化股票价值为0（默认当前未持股）
    _data['stockValue'] = 0.
    date_series = data['trade_date']
    temp = data.loc[:, ['trade_date']]
    print("trade_date shape:", temp.shape)
    _data['Date'] = temp

    print("_data.shape:", _data.shape)
    # 将处理后的数据转换为numpy数组
    _data = np.array(_data)

    # 训练数据条数
    n_train = int(np.round(_split_ratio * n_rows))
    # 测试数据条数
    n_test = n_rows - n_train

    # 训练数据集
    train = _data[:n_train]
    date_train = date_series[:n_train]
    # 测试数据集
    test = _data[-n_test:]
    print("test 1:", test[1])
    date_test = date_series[-n_test:]
    print("date_test 1:", date_test.iloc[1])
    return train, test, date_train, date_test


def data_A_process():
    return None
