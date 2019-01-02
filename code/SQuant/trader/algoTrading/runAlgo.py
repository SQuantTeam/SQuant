# encoding: utf-8

import time
import os
import json

from trader.algoTrading.sniperAlgo import SniperAlgo
from trader.gateway.tradeGateway import TradeGateway

from trader.sqSetting import *

def run_algo(algo):
    """
    run an algorithm unless it's not active
    """
    round = 0
    while algo.active:
        round += 1
        print (round)
        tick = algo.getTick(algo.symbol)
        print (tick.name)
        algo.updateTick(tick)
        algo.updateTimer()
        if algo.vtOrderID or len(algo.vtOrderID) > 0:
            time.sleep(5)
            trade = algo.tradeGateway.tdApi.qrySingleTrade(algo.vtOrderID)
            algo.updateTrade(trade)
            order = algo.tradeGateway.tdApi.qrySingleOrder(algo.vtOrderID)
            algo.updateOrder(order)

        else:
            time.sleep(5)
    algo.stop()
    # 释放连接资源
    algo.tradeGateway.close()
    return algo.tradedOrderList


def stop_algo(algo):
    algo.stop()

def save_algo(algo, setting):
    """
    save settings of user's algorithm
    """
    if not os.path.exists(algo.algorithm_param_dir):
        os.makedirs(algo.algorithm_param_dir)

    file = open(algo.algorithm_param_path, "w+")
    json.dump(setting, file, ensure_ascii=False)
    file.close()


if __name__ == "__main__":
    setting = {}
    setting['mdAddress'] = 'tcp://data.quantos.org:8910'
    setting['tdAddress'] = 'tcp://gw.quantos.org:8901'
    setting['username'] = '15827606670'
    setting['token'] = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
                       'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
    tradeGateway = TradeGateway(setting, gatewayName="squant")

    setting['symbol'] = "000718.SZ"
    setting['direction'] = DIRECTION_LONG
    setting['price'] = 3.20
    setting['volume'] = 100
    setting['offset'] = OFFSET_OPEN

    sniper_algo = SniperAlgo(tradeGateway=tradeGateway, setting=setting, email="test@test.com", algoName="sniper_test")
    print (run_algo(sniper_algo))
