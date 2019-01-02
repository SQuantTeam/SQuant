# encoding: UTF-8

from __future__ import division
from datetime import datetime
import os

from trader.sqGateway import *
from trader.sqSetting import *
from squant.settings import BASE_DIR

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
    def new(cls, tradeGateway, setting, email):
        """创建新对象"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        if timestamp != cls.timestamp:
            cls.timestamp = timestamp
            cls.count = 0
        else:
            cls.count += 1

        algoName = '_'.join([cls.templateName, cls.timestamp, str(cls.count)])
        algo = cls(tradeGateway, setting, email, algoName)
        return algo

    # ----------------------------------------------------------------------
    def __init__(self, tradeGateway, setting, email, algoName):
        """Constructor"""
        self.tradeGateway = tradeGateway
        self.active = True
        self.algoName = algoName
        self.activeOrderDict = {}  # orderID:order
        self.tradedOrderList = []  # orderID list of traded order id

        # Strategy param storage direction
        self.algorithm_param_dir = os.path.join(BASE_DIR, "output", email).replace('\\', '/')
        # Strategy param storage path
        self.algorithm_param_path = os.path.join(BASE_DIR, "output", email, algoName + ".json").replace('\\', '/')

    # ----------------------------------------------------------------------
    def updateTick(self, tick):
        """"""
        if not self.active:
            return

        self.onTick(tick)

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

        self.onTimer()

    # ----------------------------------------------------------------------
    def stop(self):
        """"""
        self.active = False
        self.cancelAll()

        self.onStop()

    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """"""
        pass

    # ----------------------------------------------------------------------
    def onTrade(self, trade):
        """"""
        pass

    # ----------------------------------------------------------------------
    def onOrder(self, order):
        """"""
        pass

    # ----------------------------------------------------------------------
    def onTimer(self):
        """"""
        pass

    # ----------------------------------------------------------------------
    def onStop(self):
        """"""
        pass

    # ----------------------------------------------------------------------
    def subscribe(self, symbol):
        """
        Do not subscribe now.
        """
        pass

    # ----------------------------------------------------------------------
    def buy(self, symbol, price, volume, priceType=None, direction=None, offset=None):
        """"""
        orderReq = SqOrderReq()
        orderReq.symbol = symbol
        code, exchange = orderReq.symbol.split('.')
        orderReq.exchange = exchange
        orderReq.price = price
        orderReq.volume = volume
        orderReq.priceType = PRICETYPE_LIMITPRICE
        orderReq.direction = direction
        orderReq.offset = offset
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





