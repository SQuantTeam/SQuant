# -*- coding: UTF-8 -*-
# encoding: utf-8
from dataapi import DataApi

if __name__ == '__main__':
    api = DataApi(addr="tcp://data.quantos.org:8910")
    phone = '15827606670'
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
    df, msg = api.login(phone, token)

    symbol = 'T1712.CFE, TF1712.CFE, rb1712.SHF'
    fields = 'open,high,low,last,volume'

    # 获取实时行情
    df, msg = api.quote(symbol=symbol, fields=fields)
    print(df)
    print(msg)