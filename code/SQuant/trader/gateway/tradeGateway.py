# encoding: UTF-8

from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object

import time
import traceback

from trader.sqGateway import *
from trader.data.dataapi import DataApi

def check_return_error(res, err_msg):
    if res is None:
        return False
    else:
        return True

# functions for generating algo parameters

#----------------------------------------------------------------------
def generateEmptyParams(security, urgency):
    """generate empty dict"""
    return {}

#----------------------------------------------------------------------
def generateVwapParams(security, urgency):
    """generate params for vwap algo"""
    params = {}
    params['urgency'] = {security: urgency}               # bid + 0.25 * bid_ask_spread
    params['participate_rate'] = {security: 0.1}
    params['price_range_factor'] = 0.1
    params['lifetime'] = 600000                     # 10 minutes
    return params

#----------------------------------------------------------------------
def generateTwapParams(security, urgency):
    """generate params for twap algo"""
    params = {}
    params['urgency'] = {security: urgency}               # bid + 0.25 * bid_ask_spread
    params['price_range_factor'] = 0.1
    params['cycle'] = 1000
    params['lifetime'] = 60000                     # 10 minutes
    return params

# 以下为一些VT类型和quantos类型的映射字典
# 价格类型映射
priceTypeMap = {}
priceTypeMap[PRICETYPE_LIMITPRICE] = ('', generateEmptyParams)
priceTypeMap[PRICETYPE_VWAP] = ('vwap', generateVwapParams)
priceTypeMap[PRICETYPE_TWAP] = ('twap', generateTwapParams)

# 动作印射
actionMap = {}
actionMap[(DIRECTION_LONG, OFFSET_OPEN)] = "Buy"
actionMap[(DIRECTION_SHORT, OFFSET_OPEN)] = "Short"
actionMap[(DIRECTION_LONG, OFFSET_CLOSE)] = "Cover"
actionMap[(DIRECTION_SHORT, OFFSET_CLOSE)] = "Sell"
actionMap[(DIRECTION_LONG, OFFSET_CLOSEYESTERDAY)] = "CoverYesterday"
actionMap[(DIRECTION_SHORT, OFFSET_CLOSEYESTERDAY)] = "SellYesterday"
actionMap[(DIRECTION_LONG, OFFSET_CLOSETODAY)] = "CoverToday"
actionMap[(DIRECTION_SHORT, OFFSET_CLOSETODAY)] = "SellToday"
actionMap[(DIRECTION_LONG, OFFSET_UNKNOWN)] = "AutoLong"
actionMap[(DIRECTION_SHORT, OFFSET_UNKNOWN)] = "AutoShort"
actionMapReverse = {v: k for k, v in list(actionMap.items())}

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

# 持仓类型映射
sideMap = {}
sideMap[DIRECTION_LONG] = 'Long'
sideMap[DIRECTION_SHORT] = 'Short'
sideMapReverse = {v:k for k,v in list(sideMap.items())}

# 产品类型映射
productClassMapReverse = {}
productClassMapReverse[1] = PRODUCT_EQUITY
productClassMapReverse[3] = PRODUCT_EQUITY
productClassMapReverse[4] = PRODUCT_EQUITY
productClassMapReverse[5] = PRODUCT_EQUITY
productClassMapReverse[8] = PRODUCT_BOND
productClassMapReverse[17] = PRODUCT_BOND
productClassMapReverse[101] = PRODUCT_FUTURES
productClassMapReverse[102] = PRODUCT_FUTURES
productClassMapReverse[103] = PRODUCT_FUTURES

# 委托状态映射
statusMapReverse = {}
statusMapReverse['New'] = STATUS_UNKNOWN
statusMapReverse['Accepted'] = STATUS_NOTTRADED
statusMapReverse['Cancelled'] = STATUS_CANCELLED
statusMapReverse['Filled'] = STATUS_ALLTRADED
statusMapReverse['Rejected'] = STATUS_REJECTED

class TradeGateway(object):
    # ----------------------------------------------------------------------
    def __init__(self, setting, gatewayName='quantos'):
        """Constructor"""
        super(TradeGateway, self).__init__()
        self.mdApi = TradeMdApi(self, setting)  # 行情
        self.tdApi = TradeTdApi(self, setting)  # 交易

        self.qryEnabled = False  # 是否要启动循环查询

        #self.dataengine = dataengine

    def connect(self):
        """To Do"""
        #self.loginWindow.show()

    def getStrategyList(self, userName, password):
        return self.tdApi.getStrategyList(userName, password)

    # ----------------------------------------------------------------------
    def login(self, username, token, selectedStrat):
        """连接"""
        try:
            # 创建行情和交易接口对象
            self.mdApi.connect(username, token)
            #self.tdApi.connect(username, token, selectedStrat)

            # 初始化并启动查询
            self.initQuery()
        except:
            traceback.print_exc()

    # ----------------------------------------------------------------------
    def subscribe(self, symbols):
        """订阅行情"""
        self.mdApi.subscribe(symbols)

    def unsubscribeAll(self):
        """订阅行情"""
        pass
        # self.mdApi.unsubscribeAll()

    # ----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        self.tdApi.sendOrder(orderReq)

    # ----------------------------------------------------------------------
    def sendBasketOrder(self, basketOrderReq):
        """"""
        return self.tdApi.sendBasketOrder(basketOrderReq)

    # ----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
        self.tdApi.cancelOrder(cancelOrderReq)

    # ----------------------------------------------------------------------
    def qryAccount(self):
        """查询账户资金"""
        self.tdApi.qryAccount()

    # ----------------------------------------------------------------------
    def qryPosition(self):
        """查询持仓"""
        self.tdApi.qryPosition()

    # ----------------------------------------------------------------------
    def close(self):
        """关闭"""
        pass
        # self.tdApi.close()

    # ----------------------------------------------------------------------
    def initQuery(self):
        """初始化连续查询"""
        if self.qryEnabled:
            # 需要循环的查询函数列表
            self.qryFunctionList = [self.qryPosition, self.qryAccount]

            self.qryCount = 0  # 查询触发倒计时
            self.qryTrigger = 2  # 查询触发点
            self.qryNextFunction = 0  # 上次运行的查询函数索引

            self.startQuery()

    # ----------------------------------------------------------------------
    def query(self, event):
        """注册到事件处理引擎上的查询函数"""
        self.qryCount += 1

        if self.qryCount > self.qryTrigger:
            # 清空倒计时
            self.qryCount = 0

            # 执行查询函数
            function = self.qryFunctionList[self.qryNextFunction]
            function()

            # 计算下次查询函数的索引，如果超过了列表长度，则重新设为0
            self.qryNextFunction += 1
            if self.qryNextFunction == len(self.qryFunctionList):
                self.qryNextFunction = 0

    # ----------------------------------------------------------------------
    def startQuery(self):
        """启动连续查询"""


    # ----------------------------------------------------------------------
    def setQryEnabled(self, qryEnabled):
        """设置是否要启动循环查询"""
        self.qryEnabled = qryEnabled


########################################################################
class TradeTdApi(object):
    #交易API实现
    def __init__(self, gateway, setting):
        """Constructor"""
        super(TradeTdApi, self).__init__()

        self.gateway = gateway  # gateway对象
        self.gatewayName = gateway.gatewayName  # gateway对象名称

        self.api = None
        self.current_stratid = None
        self.current_user = None
        self.current_strats = None

        #self.TradeApi = TradeApi

        self.setting = setting

        self.orderPricetypeDict = {}  # key:vtOrderID, value:algoType


########################################################################
class TradeMdApi(object):
    #行情接口实现
    # ----------------------------------------------------------------------
    def __init__(self, gateway, setting):
        """Constructor"""
        super(TradeMdApi, self).__init__()

        self.gateway = gateway
        self.gatewayName = gateway.gatewayName

        self.api = None

        self.fields = "OPEN,CLOSE,HIGH,LOW,LAST,\
        VOLUME,TURNOVER,OI,PRECLOSE,TIME,DATE,\
        ASKPRICE1,ASKPRICE2,ASKPRICE3,ASKPRICE4,ASKPRICE5,\
        BIDPRICE1,BIDPRICE2,BIDPRICE3,BIDPRICE4,BIDPRICE5,\
        ASKVOLUME1,ASKVOLUME2,ASKVOLUME3,ASKVOLUME4,ASKVOLUME5,\
        BIDVOLUME1,BIDVOLUME2,BIDVOLUME3,BIDVOLUME4,BIDVOLUME5,\
        LIMIT_UP,LIMIT_DOWN"

        self.fields = self.fields.replace(' ', '').lower()

        self.DataApi = DataApi

        self.setting = setting

    # ----------------------------------------------------------------------
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

            self.gateway.onTick(tick)
        except Exception as e:
            self.writeLog(u'行情更新失败，错误信息：%s' % str(e))

    # ----------------------------------------------------------------------
    def connect(self, username, token):
        """ todo """
        """连接"""
        if self.api is None:

            self.api = self.DataApi(self.setting['mdAddress'])

            # 登录
            info, msg = self.api.login(username, token)
            if check_return_error(info, msg):
                self.writeLog(u'行情连接成功')
            else:
                self.writeLog(u'行情连接失败，错误信息：%s' % msg)
        else:
            self.writeLog(u'行情已经连接')

    def unsubscribeAll(self):
        subscribed, msg = self.api.unsubscribe()

    # ----------------------------------------------------------------------
    def subscribe(self, symbols):
        """订阅"""
        subscribed, msg = self.api.subscribe(symbols, fields=self.fields, func=self.onMarketData)
        if not check_return_error(subscribed, msg):
            self.writeLog(u'行情订阅失败，错误信息：%s' % msg)

    # ----------------------------------------------------------------------
    def writeLog(self, logContent):
        """记录日志"""
        log = SqLogData()
        log.gatewayName = self.gatewayName
        log.logContent = logContent
        self.gateway.onLog(log)

    # ----------------------------------------------------------------------

    def queryInstruments(self, instcodes):

        if instcodes == "":
            df, msg = self.api.query("jz.instrumentInfo",
                                     fields="symbol, name, buylot, selllot, pricetick, multiplier, inst_type",
                                     filter="market=SH,SZ,SHF,CZC,DCE,CFE&status=1&inst_type=1,2,3,4,5,101,102,103")
        else:
            p = "symbol=%s" % instcodes
            df, msg = self.api.query("jz.instrumentInfo",
                                     fields="symbol, name, buylot, selllot, pricetick, multiplier, inst_type", filter=p)

        d = {}
        if df is None:
            return {}

        for index, row in df.iterrows():
            k = row['symbol']
            v = row
            d[k] = v
        return d

    # ----------------------------------------------------------------------
    def queryQuotes(self, instcodes):

        item_count = 50

        codelist = instcodes.split(",")

        d = {}

        symbol = ''
        for idx in range(len(codelist)):
            symbol += codelist[idx]
            symbol += ','

            if (idx == item_count):
                df, msg = self.api.quote(fields=self.fields, symbol=symbol)

                for index, row in df.iterrows():
                    k = row['symbol']
                    v = row
                    d[k] = v

                idx = 0

        if idx > 0:
            df, msg = self.api.quote(fields=self.fields, symbol=symbol)

            for index, row in df.iterrows():
                k = row['symbol']
                v = row
                d[k] = v

        return d


if __name__ == '__main__':
    setting = {}
    setting['mdAddress'] = 'tcp://data.quantos.org:8910'
    setting['tdAddress'] = 'tcp://gw.quantos.org:8901'
    setting['username'] = '15827606670'
    setting['token'] = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5N\
                       DU0NjIiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU4Mjc2MDY2NzAifQ.\
                       ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
    tradeG = TradeGateway(setting)