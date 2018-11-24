# encoding: UTF-8

from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object

import time
import traceback

from trader.data.dataapi import DataApi
from trader.trade.tradeapi import TradeApi
from trader.sqGateway import *
from trader.sqSetting import *

# 检查返回值的函数
def check_return_error(res, err_msg):
    if res is None:
        return False
    else:
        return True


class TradeGateway(object):
    # ----------------------------------------------------------------------
    def __init__(self, setting, gatewayName="SQuant"):
        """Constructor"""
        super(TradeGateway, self).__init__()
        self.gatewayName = gatewayName
        self.loginStatus = False  # 标记是否已连接到第三方交易平台
        self.mdApi = SQuantMdApi(self, setting)  # 行情
        self.tdApi = SQuantTdApi(self, setting)  # 交易
        self.login(setting['username'], setting['token'])

        # self.qryEnabled = False  # 是否要启动循环查询

    def connect(self):
        """To Do"""

    def getStrategyList(self, username, password):
        return self.tdApi.getStrategyList(username, password)

    # ----------------------------------------------------------------------
    def login(self, username, token):
        """连接"""
        try:
            # 创建行情和交易接口对象
            info = self.mdApi.connect(username, token)
            userInfo = self.tdApi.connect(username, token)
            if info is None or userInfo is None:
                self.loginStatus = False
                return
            self.loginStatus = True

        except:
            self.loginStatus = False
            traceback.print_exc()

    # ----------------------------------------------------------------------
    def qryQuote(self, instcode):
        """查询行情"""
        return self.mdApi.qryQuote(instcode=instcode)

    # ----------------------------------------------------------------------
    def qryQuoteBar(self, symbol, trade_date, freq="5M", start_time=0, end_time=160000, fields=""):
        """查询行情"""
        return self.mdApi.qryQuoteBar(symbol=symbol, trade_date=trade_date, freq=freq, start_time=start_time, end_time=end_time, fields="")

    # ----------------------------------------------------------------------
    def qryQuoteDaily(self, symbol, start_date, end_date, freq="1d", adjust_mode="post", fields=""):

        df, msg = self.mdApi.qryQuoteDaily(symbol=symbol, start_date=start_date, end_date=end_date, freq=freq, adjust_mode=adjust_mode, fields="")
        return df, msg

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
        return self.tdApi.sendOrder(orderReq)

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
        return self.tdApi.qryAccount()

    # ----------------------------------------------------------------------
    def qryPosition(self):
        """查询持仓"""
        return self.tdApi.qryPosition()

    # ----------------------------------------------------------------------
    def qryTrade(self):
        """查询持仓"""
        return self.tdApi.qryTrade()

    # ----------------------------------------------------------------------
    def qryOrder(self):
        """查询持仓"""
        return self.tdApi.qryOrder()


    # ----------------------------------------------------------------------
    def close(self):
        """关闭"""
        pass
        # self.tdApi.close()


########################################################################
class SQuantTdApi(object):
    #交易API实现
    # ----------------------------------------------------------------------
    def __init__(self, gateway, setting):
        """Constructor"""
        super(SQuantTdApi, self).__init__()

        self.gateway = gateway  # gateway对象
        self.gatewayName = gateway.gatewayName  # gateway对象名称

        self.api = None
        self.current_stratid = None
        self.current_user = None
        self.current_strats = None

        self.TradeApi = TradeApi

        self.setting = setting

        self.orderPricetypeDict = {}  # key:vtOrderID, value:algoType

    # ----------------------------------------------------------------------

    def loadContracts(self):
        """"""
        pf, msg = self.api.query_universe()

        if not check_return_error(pf, msg):
            return False

        symbols = ''
        for instcode in pf['security']:
            if len(instcode) > 0:
                symbols += str(instcode)
                symbols += ","

        instruments = self.gateway.mdApi.qryInstruments(symbols)

        for k, d in instruments.iterrows():
            contract = SqContractData()
            contract.gatewayName = self.gatewayName

            instcode = d['symbol']

            code, jzExchange = instcode.split('.')
            contract.symbol = instcode
            contract.exchange = exchangeMapReverse[jzExchange]
            contract.name = d['name']
            contract.priceTick = d['pricetick']
            contract.size = d['multiplier']
            contract.lotsize = d['buylot']
            contract.productClass = productClassMapReverse.get(int(d['inst_type']), PRODUCT_UNKNOWN)

        # do not subscribe
        # self.gateway.subscribe(symbols)
        return True

    def subscribePositionSymbols(self):
        """"""
        pf, msg = self.api.query_position()

        if not check_return_error(pf, msg):
            self.writeLog(u'查询持仓失败，错误信息：{}'.format(msg))
            return False

        symbols = ''
        for instcode in pf['security']:
            symbols += str(instcode)
            symbols += ","

        quotes = self.gateway.mdApi.qryQuotes(symbols)
        for k, d in quotes.items():
            tick = SqTickData()
            tick.gatewayName = self.gatewayName

            symbol = d['symbol']
            code, jzExchange = instcode.split('.')
            tick.symbol = symbol
            tick.exchange = exchangeMapReverse[jzExchange]
            tick.name = symbol

            tick.openPrice = d['open']
            tick.highPrice = d['high']
            tick.lowPrice = d['low']
            tick.volume = d['volume']
            tick.volchg = 0
            tick.turnover = d['turnover'] if 'turnover' in d else 0
            tick.lastPrice = d['last']

            tick.openInterest = d['oi'] if 'oi' in d else 0
            tick.preClosePrice = d['preclose'] if 'preclose' in d else 0
            tick.date = str(d['date'])

            t = str(d['time'])
            t = t.rjust(9, '0')
            tick.time = '%s:%s:%s.%s' % (t[0:2], t[2:4], t[4:6], t[6:])

            tick.bidPrice1 = d['bidprice1']
            tick.bidPrice2 = d['bidprice2']
            tick.bidPrice3 = d['bidprice3']
            tick.bidPrice4 = d['bidprice4']
            tick.bidPrice5 = d['bidprice5']

            tick.askPrice1 = d['askprice1']
            tick.askPrice2 = d['askprice2']
            tick.askPrice3 = d['askprice3']
            tick.askPrice4 = d['askprice4']
            tick.askPrice5 = d['askprice5']

            tick.bidVolume1 = d['bidvolume1']
            tick.bidVolume2 = d['bidvolume2']
            tick.bidVolume3 = d['bidvolume3']
            tick.bidVolume4 = d['bidvolume4']
            tick.bidVolume5 = d['bidvolume5']

            tick.askVolume1 = d['askvolume1']
            tick.askVolume2 = d['askvolume2']
            tick.askVolume3 = d['askvolume3']
            tick.askVolume4 = d['askvolume4']
            tick.askVolume5 = d['askvolume5']

            tick.upperLimit = d['limit_up'] if 'limit_up' in d else 0
            tick.lowerLimit = d['limit_down'] if 'limit_down' in d else 0

            self.gateway.onTick(tick)

        self.gateway.subscribe(symbols)

        return True

    # ----------------------------------------------------------------------
    def onOrderStatus(self, data):
        """委托信息推送"""
        order = SqOrderData()
        order.gatewayName = self.gatewayName

        code, exchange = data['security'].split('.')
        order.symbol = data['security']

        instruments = self.gateway.mdApi.qryInstruments(order.symbol)  # only one symbol here
        order.name = instruments.loc[0, 'name']
        order.exchange = exchangeMapReverse.get(exchange, EXCHANGE_UNKNOWN)

        order.orderID = str(data['entrust_no'])
        order.taskID = str(data['task_id'])
        order.vtOrderID = order.orderID

        order.direction, order.offset = actionMapReverse.get(data['entrust_action'],
                                                             (DIRECTION_UNKNOWN, OFFSET_UNKNOWN))
        order.totalVolume = data['entrust_size']
        order.tradedVolume = data['fill_size']
        order.price = data['entrust_price']
        order.status = statusMapReverse.get(data['order_status'])

        # addtional info
        order.tradePrice = data['fill_price']

        t = str(data['entrust_time'])
        t = t.rjust(6, '0')
        order.orderTime = '%s:%s:%s' % (t[0:2], t[2:4], t[4:])

        # if order.vtOrderID in self.orderPricetypeDict:
        # order.priceType = self.orderPricetypeDict[order.vtOrderID]
        order.priceType = data['algo']

        return order


    # ----------------------------------------------------------------------
    def onTrade(self, data):
        """成交信息推送"""
        trade = SqTradeData()
        trade.gatewayName = self.gatewayName

        code, jzExchange = data['security'].split('.')
        trade.symbol = data['security']

        instruments = self.gateway.mdApi.qryInstruments(trade.symbol)  # only one symbol here
        trade.name = instruments.loc[0, 'name']
        trade.exchange = exchangeMapReverse.get(jzExchange, EXCHANGE_UNKNOWN)

        trade.direction, trade.offset = actionMapReverse.get(data['entrust_action'],
                                                             (DIRECTION_UNKNOWN, OFFSET_UNKNOWN))

        trade.tradeID = str(data['fill_no'])
        trade.vtTradeID = str(data['fill_no'])

        trade.orderID = str(data['entrust_no'])
        trade.vtOrderID = trade.orderID
        trade.taskID = str(data['task_id'])

        trade.price = data['fill_price']
        trade.volume = data['fill_size']

        t = str(data['fill_time'])
        t = t.rjust(6, '0')
        trade.tradeTime = '%s:%s:%s' % (t[0:2], t[2:4], t[4:])

        return trade

    # ----------------------------------------------------------------------
    def onConnection(self, data):
        """"""
        self.writeLog(u'连接状态更新：%s' % data)

    def getStrategyList(self, username, token):

        if self.api is None:
            tdAddress = self.setting['tdAddress']
            self.api = self.TradeApi(tdAddress)

            # 登录
            info, msg = self.api.login(username, token)

            if check_return_error(info, msg):
                self.writeLog(u'登录成功')
                self.current_strats = info['strategies']
                self.current_user = info['username']
                return info['strategies']
            # if info is None:
            else:
                self.writeLog(u'登录失败，错误信息：%s' % msg)
                self.api = None
                return None
        else:
            self.writeLog(u'已经登录')
            return self.current_strats

    # ----------------------------------------------------------------------
    def connect(self, username, password):
        """初始化连接"""
        # 创建API对象并绑定回调函数
        tdAddress = self.setting['tdAddress']
        self.api = self.TradeApi(tdAddress)
        # 设置回调函数
        self.api.set_ordstatus_callback(on_orderstatus)
        self.api.set_trade_callback(on_trade)
        self.api.set_task_callback(on_taskstatus)
        # 登录
        userInfo, msg = self.api.login(username, password)
        if userInfo is None:
            return userInfo
        userStrats = userInfo['strategies']
        # print (userStrats)
        sid, msg = self.api.use_strategy(userStrats[0])
        return userInfo


    # ----------------------------------------------------------------------
    def close(self):
        """关闭"""
        pass

    # ----------------------------------------------------------------------
    def writeLog(self, logContent):
        """记录日志"""
        log = SqLogData()
        log.gatewayName = self.gatewayName
        log.logContent = logContent

    # ----------------------------------------------------------------------
    def sendOrder(self, orderReq):
        """发单"""
        security = orderReq.symbol
        urgency = orderReq.urgency
        algo, paramsFunction = priceTypeMap[orderReq.priceType]

        if len(orderReq.offset) > 0:
            action = actionMap.get((orderReq.direction, orderReq.offset), '')
            if len(algo) > 0:
                taskid, msg = self.api.place_order(security, action, orderReq.price, int(orderReq.volume), algo,
                                                   paramsFunction(security, urgency))
            else:
                taskid, msg = self.api.place_order(security, action, orderReq.price, int(orderReq.volume))
        else:
            inc_size = int(orderReq.volume) if orderReq.direction == DIRECTION_LONG else int(orderReq.volume) * -1

            taskid, msg = self.api.batch_order([{"security": security, "price": orderReq.price, "size": inc_size}],
                                               algo, paramsFunction(security, urgency))
        return taskid, msg

    # ----------------------------------------------------------------------
    def sendBasketOrder(self, req):
        """
        when sending basket order, taskid is returned instead of vtOrderID
        """
        taskid, msg = self.api.basket_order(req.positions, req.algo, req.params)

        # return result
        if not check_return_error(taskid, msg):
            self.writeLog(u'篮子委托失败，错误信息：%s' % msg)
            return None
        else:
            return str(taskid)

    # ----------------------------------------------------------------------
    def cancelOrder(self, cancelOrderReq):
        """撤单"""
        if not self.api:
            return

        result, msg = self.api.cancel_order(cancelOrderReq.orderID)

        if not check_return_error(result, msg):
            self.writeLog(u'撤单失败，错误信息：%s' % msg)

    # ----------------------------------------------------------------------
    def qryPosition(self):
        """查询持仓"""
        df, msg = self.api.query_position()
        positionList = []
        if df is None:
            return positionList

        for index, data in df.iterrows():
            position = SqPositionData()
            position.gatewayName = self.gatewayName

            code, jzExchange = data['security'].split('.')
            position.symbol = data['security']

            instruments = self.gateway.mdApi.qryInstruments(position.symbol)   # only one symbol here
            position.name = instruments.loc[0, 'name']

            position.exchange = exchangeMapReverse.get(jzExchange, EXCHANGE_UNKNOWN)

            position.direction = sideMapReverse.get(data['side'], DIRECTION_UNKNOWN)
            position.vtPositionName = '.'.join([data['security'], position.direction])

            position.price = data['cost_price']
            position.ydPosition = data['pre_size']
            position.tdPosition = data['today_size']
            position.position = data['current_size']
            position.frozen = data['frozen_size']

            position.commission = data['commission']
            position.enable = data['enable_size']
            position.want = data['want_size']
            position.initPosition = data['init_size']
            position.trading = data['trading_pnl']
            position.holding = data['holding_pnl']
            position.last = data['last_price']

            if (position.position > 0):
                if not instruments.empty:
                    # instruments.loc[0, "multiplier"] is the same as "contract.size"
                    position.mktval = data['last_price'] * position.position * instruments.loc[0, "multiplier"]
                else:
                    position.mktval = 0.0

            positionList.append(position)

        return positionList

    def qryAccount(self):

        df, msg = self.api.query_account()
        account = SqAccountData()
        if df is None:
            return account
        for index, data in df.iterrows():
            account.accountID = data['id']
            account.type = data['type']
            account.vtAccountID = str(data['id']) + "_" + data['type']

            account.frozen_balance = data['frozen_balance']
            account.enable_balance = data['enable_balance']
            account.float_pnl = data['float_pnl']
            account.init_balance = data['init_balance']
            account.deposit_balance = data['deposit_balance']
            account.holding_pnl = data['holding_pnl']
            account.close_pnl = data['close_pnl']
            account.margin = data['margin']
            account.trading_pnl = data['trading_pnl']

        return account

    # ----------------------------------------------------------------------
    def qryOrder(self):
        """查询委托"""
        df, msg = self.api.query_order()
        orderList = []

        if not check_return_error(df, msg):
            return orderList

        for index, data in df.iterrows():
            order = self.onOrderStatus(data)
            orderList.append(order)

        return orderList

    # ----------------------------------------------------------------------
    def qryTrade(self):
        """查询成交"""
        df, msg = self.api.query_trade()
        tradeList = []

        if not check_return_error(df, msg):
            return tradeList

        for index, data in df.iterrows():
            trade = self.onTrade(data)
            tradeList.append(trade)

        return tradeList


########################################################################
class SQuantMdApi(object):
    #行情接口实现
    # ----------------------------------------------------------------------
    def __init__(self, gateway, setting):
        """Constructor"""
        super(SQuantMdApi, self).__init__()

        self.gateway = gateway
        self.gatewayName = gateway.gatewayName

        self.api = None

        self.fields = "SYMBOL,OPEN,CLOSE,HIGH,LOW,LAST,\
        VOLUME,TURNOVER,OI,PRECLOSE,TIME,DATE,\
        TRADE_DATE,VWAP,SETTLE,IOPV,PRESETTLE,PREOI,\
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

        except Exception as e:
            self.writeLog(u'行情更新失败，错误信息：%s' % str(e))

    # ----------------------------------------------------------------------
    def connect(self, username, token):
        """连接"""
        if self.api is None:
            self.api = self.DataApi(self.setting['mdAddress'], use_jrpc=False)
        # 登录
        info, msg = self.api.login(username, token)
        return info

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

    # ----------------------------------------------------------------------

    def qryInstruments(self, instcodes):

        if instcodes == "":
            df, msg = self.api.query("jz.instrumentInfo",
                                     fields="symbol, name, buylot, selllot, pricetick, multiplier, inst_type",
                                     filter="market=SH,SZ,SHF,CZC,DCE,CFE&status=1&inst_type=1,2,3,4,5,101,102,103")
        else:
            p = "symbol=%s" % instcodes
            df, msg = self.api.query("jz.instrumentInfo",
                                     fields="symbol, name, buylot, selllot, pricetick, multiplier, inst_type", filter=p)
        return df

    # ----------------------------------------------------------------------
    def qryQuote(self, instcode):

        df, msg = self.api.quote(fields=self.fields, symbol=instcode)
        tick = SqTickData()
        if df.empty:
            return tick
        for index, d in df.iterrows():
            instruments = self.gateway.mdApi.qryInstruments(d['symbol'])
            tick.name = instruments.loc[0, "name"]
            tick.gatewayName = self.gatewayName

            symbol = d['symbol']
            code, jzExchange = instcode.split('.')
            tick.symbol = symbol
            tick.exchange = exchangeMapReverse[jzExchange]

            tick.openPrice = d['open']
            tick.highPrice = d['high']
            tick.lowPrice = d['low']
            tick.volume = d['volume']
            tick.lastVolume = 0
            tick.volchg = 0
            tick.turnover = d['turnover'] if 'turnover' in d else 0
            tick.lastPrice = d['last']

            tick.openInterest = d['oi'] if 'oi' in d else 0
            tick.preClosePrice = d['preclose'] if 'preclose' in d else 0
            tick.date = str(d['date'])
            tick.tradeDate = str(d['trade_date'])

            tick.settlePrice = d['settle']
            tick.preSettlePrice = d['presettle']
            tick.preOpenInterest = d['preoi']
            tick.closePrice = d['close']
            tick.vwap = d['vwap']
            tick.iopv = d['iopv'] if 'iopv' in d else 0

            t = str(d['time'])
            t = t.rjust(9, '0')
            tick.time = '%s:%s:%s.%s' % (t[0:2], t[2:4], t[4:6], t[6:])

            tick.bidPrice1 = d['bidprice1']
            tick.bidPrice2 = d['bidprice2']
            tick.bidPrice3 = d['bidprice3']
            tick.bidPrice4 = d['bidprice4']
            tick.bidPrice5 = d['bidprice5']

            tick.askPrice1 = d['askprice1']
            tick.askPrice2 = d['askprice2']
            tick.askPrice3 = d['askprice3']
            tick.askPrice4 = d['askprice4']
            tick.askPrice5 = d['askprice5']

            tick.bidVolume1 = d['bidvolume1']
            tick.bidVolume2 = d['bidvolume2']
            tick.bidVolume3 = d['bidvolume3']
            tick.bidVolume4 = d['bidvolume4']
            tick.bidVolume5 = d['bidvolume5']

            tick.askVolume1 = d['askvolume1']
            tick.askVolume2 = d['askvolume2']
            tick.askVolume3 = d['askvolume3']
            tick.askVolume4 = d['askvolume4']
            tick.askVolume5 = d['askvolume5']

            tick.upperLimit = d['limit_up'] if 'limit_up' in d else 0
            tick.lowerLimit = d['limit_down'] if 'limit_down' in d else 0

        return tick

    # ----------------------------------------------------------------------
    def qryQuoteBar(self, symbol, trade_date, freq="5M", start_time=0, end_time=160000, fields=""):

        df, msg = self.api.bar(symbol=symbol, trade_date=trade_date, freq=freq, start_time=start_time, end_time=end_time, fields="")
        return df, msg

    # ----------------------------------------------------------------------
    def qryQuoteDaily(self, symbol, start_date, end_date, freq="1d", adjust_mode="post", fields=""):

        df, msg = self.api.daily(symbol=symbol, start_date=start_date, end_date=end_date, freq=freq, adjust_mode=adjust_mode, fields="")
        return df, msg

########################################################################
    # TradeApi通过回调函数方式通知用户事件。事件包括三种：订单状态、成交回报、委托任务执行状态。

    # 订单状态推送
def on_orderstatus(order):
    print("on_orderstatus:")  # , order
    # for key in order:    print("%20s : %s" % (key, str(order[key])))
    print("")

# 成交回报推送
def on_trade(trade):
    print("on_trade:")
    # for key in trade:    print("%20s : %s" % (key, str(trade[key])))
    print("")

# 委托任务执行状态推送
# 通常可以忽略该回调函数
def on_taskstatus(task):
    print("on_taskstatus:")
    # for key in task:    print("%20s : %s" % (key, str(task[key])))
    print("")


if __name__ == '__main__':
    setting = {}
    setting['mdAddress'] = 'tcp://data.quantos.org:8910'
    setting['tdAddress'] = 'tcp://gw.quantos.org:8901'
    setting['username'] = '15827606670'
    setting['token'] = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
                        'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
    tradeG = TradeGateway(setting, gatewayName="SQuant")
    # print (tradeG.loginStatus)
    # tradeG.login(setting['username'], setting['token'])

    # print(tradeG.qryQuote("000001.SH").name)

    # account = tradeG.qryAccount()
    # print (account.vtAccountID)

    # print(tradeG.mdApi.queryInstruments("000001.SH").loc[0, "name"])
    # print (tradeG.tdApi.qryAccount().accountID)

    # positionList = tradeG.tdApi.qryPosition()
    # for i in positionList:
    #     print i.mktval

    # orderList = tradeG.qryOrder()
    # for i in orderList:
    #     print i.name

    # tradeList = tradeG.tdApi.qryTrade()
    # for i in tradeList:
    #     print i.orderID

    # orderReq = SqOrderReq()
    # orderReq.symbol = '000001.SH'
    # code, exchange = orderReq.symbol.split('.')
    # orderReq.exchange = exchange
    # orderReq.price = 2643.0001
    # orderReq.volume = 400
    # orderReq.urgency = 0
    # orderReq.priceType = PRICETYPE_LIMITPRICE
    # orderReq.direction = DIRECTION_LONG
    # orderReq.offset = OFFSET_OPEN
    #
    # taskid, msg = tradeG.sendOrder(orderReq)
    # print (taskid, msg)

    # df, msg = tradeG.qryQuoteBar(symbol='000001.SH', trade_date='2018-11-23')
    # print (df)

    df, msg = tradeG.qryQuoteDaily(symbol='000001.SH', start_date='2018-11-01', end_date='2018-11-20')
    print (df)

