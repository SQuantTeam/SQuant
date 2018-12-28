# -*- coding: UTF-8 -*-
# encoding: UTF-8

from trader.algoTrading.sniperAlgo import SniperAlgo
from trader.gateway.tradeGateway import TradeGateway
from trader.sqConstant import *

if __name__ == '__main__':
    userSetting = {}
    userSetting['mdAddress'] = 'tcp://data.quantos.org:8910'
    userSetting['tdAddress'] = 'tcp://gw.quantos.org:8901'
    userSetting['username'] = '15827606670'
    userSetting['token'] = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
                       'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
    tradeG = TradeGateway(userSetting, gatewayName='squant')
    print (tradeG.loginStatus)

    algoSetting = {}
    algoSetting['symbol'] = '000001.SZ'
    algoSetting['direction'] = DIRECTION_LONG
    algoSetting['price'] = 1000
    algoSetting['volume'] = 200
    algoSetting['offset'] = OFFSET_OPEN

    sniperAlgoInstance = SniperAlgo.new(tradeG, algoSetting)
    print (sniperAlgoInstance.algoName)
    tradeG.close()
