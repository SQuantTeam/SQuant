# encoding: UTF-8

from __future__ import division
from collections import OrderedDict

from six import text_type

from trader.sqSetting import *
from trader.algoTrading.algoTemplate import AlgoTemplate

STATUS_FINISHED = set([STATUS_ALLTRADED, STATUS_CANCELLED, STATUS_REJECTED])


########################################################################
class SniperAlgo(AlgoTemplate):
    """狙击手算法"""

    templateName = u'Sniper 狙击手'

    # ----------------------------------------------------------------------
    def __init__(self, tradeGateway, setting, algoName):
        """Constructor"""
        super(SniperAlgo, self).__init__(tradeGateway, setting, algoName)

        # 参数，强制类型转换，保证从CSV加载的配置正确
        self.symbol = str(setting['symbol'])  # 合约代码
        self.direction = text_type(setting['direction'])  # 买卖
        self.price = float(setting['price'])  # 价格
        self.volume = float(setting['volume'])  # 数量
        self.offset = text_type(setting['offset'])  # 开平

        self.vtOrderID = ''  # 委托号
        self.tradedVolume = 0  # 成交数量


    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """"""
        # 执行撤单
        if self.vtOrderID:
            self.cancelAll()
            return

        # 做多，且卖1价格小于等于执行目标价
        if (self.direction == DIRECTION_LONG and
             tick.askPrice1 <= self.price):
            orderVolume = self.volume - self.tradedVolume
            orderVolume = min(orderVolume, tick.askVolume1)
            self.vtOrderID = self.buy(self.symbol, self.price,
                                      orderVolume, offset=self.offset)

        # 做空
        elif (self.direction == DIRECTION_SHORT and
               tick.bidPrice1 >= self.price):
            orderVolume = self.volume - self.tradedVolume
            orderVolume = min(orderVolume, tick.bidVolume1)
            self.vtOrderID = self.sell(self.symbol, self.price,
                                       orderVolume, offset=self.offset)



    # ----------------------------------------------------------------------
    def onTrade(self, trade):
        """"""
        self.tradedVolume += trade.volume

        if self.tradedVolume >= self.volume:
            self.stop()


    # ----------------------------------------------------------------------
    def onOrder(self, order):
        """"""
        # 若委托已经结束，则清空委托号
        if order.status in STATUS_FINISHED:
            self.vtOrderID = ''


    # ----------------------------------------------------------------------
    def onTimer(self):
        """"""
        pass

    # ----------------------------------------------------------------------
    def onStop(self):
        """"""
        pass

