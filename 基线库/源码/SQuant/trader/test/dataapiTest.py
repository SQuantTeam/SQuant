# -*- coding: UTF-8 -*-
# encoding: utf-8

import pandas as pd

from trader.data.dataapi import DataApi
from trader.sqGateway import *

# 交易所类型映射
exchangeMap = {}
exchangeMap[EXCHANGE_CFFEX] = 'CFE'
exchangeMap[EXCHANGE_SHFE] = 'SHF'
exchangeMap[EXCHANGE_CZCE] = 'CZC'
exchangeMap[EXCHANGE_DCE] = 'DCE'
exchangeMap[EXCHANGE_SSE] = 'SH'
exchangeMap[EXCHANGE_SZSE] = 'SZ'
exchangeMap[EXCHANGE_SGE] = 'SGE'
exchangeMap[EXCHANGE_CSI] = 'CSI'
exchangeMap[EXCHANGE_HKS] = 'HKS'
exchangeMap[EXCHANGE_HKH] = 'HKH'
exchangeMap[EXCHANGE_JZ] = 'JZ'
exchangeMap[EXCHANGE_SPOT] = 'SPOT'
exchangeMap[EXCHANGE_IB] = 'IB'
exchangeMap[EXCHANGE_FX] = 'FX'
exchangeMap[EXCHANGE_INE] = 'INE'

exchangeMapReverse = {v:k for k,v in list(exchangeMap.items())}

def onMarketData(self, key, data):
    """行情推送"""
    tick = SqTickData()
    tick.gatewayName = self.gatewayName

    try:
        l = data['symbol'].split('.')
        tick.symbol = data['symbol']
        tick.name = data['symbol']
        tick.exchange = exchangeMapReverse.get(l[1], EXCHANGE_UNKNOWN)

        tick.openPrice = data['open']
        tick.highPrice = data['high']
        tick.lowPrice = data['low']
        tick.volume = data['volume']
        tick.volchg = 0
        tick.turnover = data['turnover'] if 'turnover' in data else 0
        tick.lastPrice = data['last']

        tick.openInterest = data['oi'] if 'oi' in data else 0
        tick.preClosePrice = data['preclose'] if 'preclose' in data else 0
        tick.date = str(data['date'])

        t = str(data['time'])
        t = t.rjust(9, '0')
        tick.time = '%s:%s:%s.%s' % (t[0:2], t[2:4], t[4:6], t[6:])

        tick.bidPrice1 = data['bidprice1']
        tick.bidPrice2 = data['bidprice2']
        tick.bidPrice3 = data['bidprice3']
        tick.bidPrice4 = data['bidprice4']
        tick.bidPrice5 = data['bidprice5']

        tick.askPrice1 = data['askprice1']
        tick.askPrice2 = data['askprice2']
        tick.askPrice3 = data['askprice3']
        tick.askPrice4 = data['askprice4']
        tick.askPrice5 = data['askprice5']

        tick.bidVolume1 = data['bidvolume1']
        tick.bidVolume2 = data['bidvolume2']
        tick.bidVolume3 = data['bidvolume3']
        tick.bidVolume4 = data['bidvolume4']
        tick.bidVolume5 = data['bidvolume5']

        tick.askVolume1 = data['askvolume1']
        tick.askVolume2 = data['askvolume2']
        tick.askVolume3 = data['askvolume3']
        tick.askVolume4 = data['askvolume4']
        tick.askVolume5 = data['askvolume5']

        tick.upperLimit = data['limit_up'] if 'limit_up' in data else 0
        tick.lowerLimit = data['limit_down'] if 'limit_down' in data else 0

    except Exception as e:
        self.writeLog(u'行情更新失败，错误信息：%s' % str(e))


if __name__ == '__main__':
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    api = DataApi(addr="tcp://data.quantos.org:8910")
    phone = '15827606670'
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU4Mj' \
    'c2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
    df, msg = api.login(phone, token)
    print(df, msg)

    df, msg = api.query(view="help.apiParam", filter="param=pe")
    print (df)

    # symbol = '000718.SZ'
    # fields = "OPEN,CLOSE,HIGH,LOW,LAST,\
    #         VOLUME,TURNOVER,OI,PRECLOSE,TIME,DATE,\
    #         LIMIT_UP,LIMIT_DOWN"
    # fields = fields.replace(' ', '').lower()
    #
    # # 获取实时行情
    # df, msg = api.quote(symbol=symbol, fields=fields)
    # print ('here', df)
    # print(df.to_json(orient='records'))
    #
    # #获取k线图
    # df, msg = api.bar(
    #     symbol="600030.SH",
    #     trade_date=20181116,
    #     freq="5M",
    #     start_time=0,
    #     end_time=160000,
    #     fields="")
    # df.to_csv('df.csv')
    # print(df.to_json(orient='records'))
    # print(msg)
    #
    # api.close()
    #
    # # 获取k线图
    # df, msg = api.bar(
    #     symbol="600030.SH",
    #     trade_date=20181116,
    #     freq="5M",
    #     start_time=0,
    #     end_time=160000,
    #     fields="")
    # print(df.to_json(orient='records'))
    # print(msg)
    #
    # df, msg = api.query("jz.instrumentInfo",
    #                          fields="symbol, name, buylot, selllot, pricetick, multiplier, inst_type",
    #                          filter="market=SH,SZ,SHF,CZC,DCE,CFE&status=1&inst_type=1,2,3,4,5,101,102,103")
    #
    # df.to_csv("instrument.csv", encoding = "utf-8")