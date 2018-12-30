# -*- coding: UTF-8 -*-
# encoding: UTF-8

from __future__ import division
from datetime import datetime

from trader.sqGateway import *
from trader.sqSetting import *

# 活动委托状态
STATUS_ACTIVE = [STATUS_NOTTRADED, STATUS_PARTTRADED, STATUS_UNKNOWN]


########################################################################
class AlgoTemplate(object):
    """交易算法模板"""
    templateName = 'AlgoTemplate'

    timestamp = ''
    count = 0

    @classmethod
    # ----------------------------------------------------------------------
    def new(cls, tradeGateway, setting):
        """创建新对象"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        if timestamp != cls.timestamp:
            cls.timestamp = timestamp
            cls.count = 0
        else:
            cls.count += 1

        algoName = '_'.join([cls.templateName, cls.timestamp, str(cls.count)])
        algo = cls(tradeGateway, setting, algoName)
        return algo

    # ----------------------------------------------------------------------
    def __init__(self, tradeGateway, setting, algoName):
        """Constructor"""
        self.tradeGateway = tradeGateway
        self.active = True
        self.algoName = algoName
        self.activeOrderDict = {}  # orderID:order

    # ----------------------------------------------------------------------
    def updateTick(self, tick):
        """"""
        if not self.active:
            return

        return self.tradeGateway.qryQuote(tick.symbol)

    # ----------------------------------------------------------------------
    def updateTrade(self, trade):
        """"""
        if not self.active:
            return

        self.onTrade(trade)

    # ----------------------------------------------------------------------
    def updateOrder(self, order):
        """"""
        if not self.active:
            return

        # 活动委托需要缓存
        if order.status in STATUS_ACTIVE:
            self.activeOrderDict[order.vtOrderID] = order
        # 结束委托需要移除
        elif order.vtOrderID in self.activeOrderDict:
            del self.activeOrderDict[order.vtOrderID]

        self.onOrder(order)

    # ----------------------------------------------------------------------
    def updateTimer(self):
        """"""
        if not self.active:
            return

        # Todo

    # ------------------
    # ----------------------------------------------------
    def stop(self):
        """"""
        self.active = False
        self.cancelAll()

    # ----------------------------------------------------------------------
    def buy(self, symbol, price, volume, priceType=None, offset=None):
        """"""
        orderReq = SqOrderReq()
        orderReq.symbol = symbol
        code, exchange = orderReq.symbol.split('.')
        orderReq.exchange = exchange
        orderReq.price = price
        orderReq.volume = volume
        orderReq.priceType = None
        orderReq.direction = DIRECTION_LONG
        orderReq.offset = OFFSET_OPEN
        return self.tradeGateway.sendOrder(orderReq)

    # ----------------------------------------------------------------------
    def sell(self, symbol, price, volume, priceType=None, offset=None):
        """"""
        orderReq = SqOrderReq()
        orderReq.symbol = symbol
        code, exchange = orderReq.symbol.split('.')
        orderReq.exchange = exchange
        orderReq.price = price
        orderReq.volume = volume
        orderReq.priceType = None
        orderReq.direction = DIRECTION_SHORT
        orderReq.offset = OFFSET_CLOSE
        return self.tradeGateway.sendOrder(orderReq)

    # ----------------------------------------------------------------------
    def cancelOrder(self, orderID):
        """"""
        cancelOrderReq = SqCancelOrderReq()
        cancelOrderReq.orderID = orderID
        self.tradeGateway.cancelOrder(cancelOrderReq)

    # ----------------------------------------------------------------------
    def cancelAll(self):
        """"""
        if not self.activeOrderDict:
            return False

        for order in self.activeOrderDict.values():
            self.cancelOrder(order.vtOrderID)
        return True

    # ----------------------------------------------------------------------
    def getTick(self, symbol):
        """"""
        return self.tradeGateway.qryQuote(symbol)

        # ----------------------------------------------------------------------

    def getContract(self, symbol):
        """"""
        return self.tradeGateway.getContract(symbol)

    # ----------------------------------------------------------------------

    def roundValue(self, value, change):
        """标准化价格或者数量"""
        if not change:
            return value

        n = value / change
        v = round(n, 0) * change
        return v

    # ----------------------------------------------------------------------

    def varEvent(self, value, change):
        """"""
        pass



