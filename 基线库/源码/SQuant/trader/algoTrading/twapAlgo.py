# -*- coding: UTF-8 -*-
# encoding: UTF-8

from __future__ import division
from collections import OrderedDict

from six import text_type

from trader.sqSetting import *
from .algoTemplate import AlgoTemplate


########################################################################
class TwapAlgo(AlgoTemplate):
    """TWAP算法"""

    templateName = u'TWAP 时间加权平均'

    # ----------------------------------------------------------------------
    def __init__(self, engine, setting, algoName):
        """Constructor"""
        super(TwapAlgo, self).__init__(engine, setting, algoName)

        # 参数，强制类型转换，保证从CSV加载的配置正确
        self.symbol = str(setting['symbol'])  # 合约代码
        self.direction = text_type(setting['direction'])  # 买卖
        self.targetPrice = float(setting['targetPrice'])  # 目标价格
        self.totalVolume = float(setting['totalVolume'])  # 总数量
        self.time = int(setting['time'])  # 执行时间
        self.interval = int(setting['interval'])  # 执行间隔
        self.minVolume = float(setting['minVolume'])  # 最小委托数量
        self.priceLevel = int(setting['priceLevel'])  # 使用第几档价格委托

        # 变量
        self.orderSize = self.totalVolume / (self.time / self.interval)
        self.orderSize = self.roundValue(self.orderSize, self.minVolume)
        if self.minVolume >= 1:
            self.orderSize = int(self.orderSize)

        self.timerCount = 0
        self.timerTotal = 0
        self.tradedVolume = 0

        self.subscribe(self.symbol)


    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """"""
        pass

    # ----------------------------------------------------------------------
    def onTrade(self, trade):
        """"""
        self.tradedVolume += trade.volume

        if self.tradedVolume >= self.totalVolume:
            self.stop()
        else:
            pass

    # ----------------------------------------------------------------------
    def onOrder(self, order):
        """"""
        pass

    # ----------------------------------------------------------------------
    def onTimer(self):
        """"""
        self.timerCount += 1
        self.timerTotal += 1

        # 总时间结束，停止算法
        if self.timerTotal >= self.time:
            self.stop()
            return

        # 每到间隔发一次委托
        if self.timerCount >= self.interval:
            self.timerCount = 0

            tick = self.getTick(self.symbol)
            if not tick:
                return

            size = min(self.orderSize, self.totalVolume - self.tradedVolume)

            # 买入
            if self.direction == DIRECTION_LONG:
                # 市场买1价小于目标买价
                if tick.bidPrice1 < self.targetPrice:
                    # 计算委托价格
                    priceMap = {
                        1: tick.askPrice1,
                        2: tick.askPrice2,
                        3: tick.askPrice3,
                        4: tick.askPrice4,
                        5: tick.askPrice5,
                    }
                    price = priceMap[self.priceLevel]
                    if price:
                        price = min(price, self.targetPrice)  # 如果深度价格为0，则使用目标价
                    else:
                        price = self.targetPrice

                    # 发出委托
                    self.buy(self.symbol, price, size)
                    self.writeLog(u'委托买入%s，数量%s，价格%s' % (self.symbol, self.orderSize, price))
            # 卖出
            if self.direction == DIRECTION_SHORT:
                # 市场卖1价大于目标价
                if tick.askPrice1 > self.targetPrice:
                    # 计算委托价格
                    priceMap = {
                        1: tick.bidPrice1,
                        2: tick.bidPrice2,
                        3: tick.bidPrice3,
                        4: tick.bidPrice4,
                        5: tick.bidPrice5,
                    }
                    price = priceMap[self.priceLevel]
                    if price:
                        price = max(price, self.targetPrice)
                    else:
                        price = self.targetPrice

                    # 发出委托
                    self.sell(self.symbol, price, size)
                    self.writeLog(u'委托卖出%s，数量%s，价格%s' % (self.symbol, self.orderSize, price))

        # 委托后等待到间隔一半的时间撤单
        elif self.timerCount == round(self.interval / 2, 0):
            result = self.cancelAll()
            if result:
                self.writeLog(u'撤销之前的委托')

        self.varEvent()

    # ----------------------------------------------------------------------
    def onStop(self):
        """"""
        self.writeLog(u'运行时间已到，停止算法')
        self.varEvent()

    # ----------------------------------------------------------------------
    def varEvent(self):
        """更新变量"""
        d = OrderedDict()
        d[u'算法状态'] = self.active
        d[u'成交数量'] = self.tradedVolume
        d[u'单笔委托'] = self.orderSize
        d[u'本轮读秒'] = self.timerCount
        d[u'累计读秒'] = self.timerTotal
        d['active'] = self.active
        self.putVarEvent(d)

    # ----------------------------------------------------------------------
    def paramEvent(self):
        """更新参数"""
        d = OrderedDict()
        d[u'代码'] = self.symbol
        d[u'方向'] = self.direction
        d[u'目标价格'] = self.targetPrice
        d[u'总数量'] = self.totalVolume
        d[u'总时间（秒）'] = self.time
        d[u'间隔（秒）'] = self.interval
        d[u'委托档位'] = self.priceLevel
        self.putParamEvent(d)
