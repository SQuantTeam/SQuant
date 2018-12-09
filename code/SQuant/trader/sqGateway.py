# encoding: UTF-8

from builtins import str
from builtins import object

import time

from sqConstant import *

########################################################################


########################################################################
class SqBaseData(object):
    """回调函数推送数据的基础类，其他数据类继承于此"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.gatewayName = EMPTY_STRING  # Gateway名称
        self.rawData = None  # 原始数据


########################################################################
class SqTickData(SqBaseData):
    """Tick行情数据类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(SqTickData, self).__init__()

        # 代码相关
        self.symbol = EMPTY_STRING  # 合约代码
        self.exchange = EMPTY_STRING  # 交易所代码
        self.name = EMPTY_STRING  # 代码名称

        # 成交数据
        self.lastPrice = EMPTY_FLOAT  # 最新成交价
        self.lastVolume = EMPTY_INT  # 最新成交量
        self.volume = EMPTY_INT  # 今天总成交量
        self.volchg = EMPTY_INT  # 今天总成交量
        self.turnover = EMPTY_LONG  # 今天总成交额
        self.openInterest = EMPTY_INT  # 持仓量
        self.time = EMPTY_STRING  # 时间 11:20:56.5
        self.date = EMPTY_STRING  # 日期 20181009
        self.tradeDate = EMPTY_STRING  # 日期 20181009

        self.settlePrice = EMPTY_FLOAT  # 今结算价
        self.preSettlePrice = EMPTY_FLOAT  # 昨结算价
        self.preOpenInterest = EMPTY_FLOAT  #昨持仓

        # 常规行情
        self.openPrice = EMPTY_FLOAT  # 今日开盘价
        self.highPrice = EMPTY_FLOAT  # 今日最高价
        self.lowPrice = EMPTY_FLOAT  # 今日最低价
        self.preClosePrice = EMPTY_FLOAT

        self.closePrice = EMPTY_FLOAT  # 收盘价
        self.vwap = EMPTY_FLOAT  # 当日平均成交均价，计算公式为成交金额除以成交量
        self.iopv = EMPTY_FLOAT  # IOPV净值估值（基金概念）

        self.upperLimit = EMPTY_FLOAT  # 涨停价
        self.lowerLimit = EMPTY_FLOAT  # 跌停价

        # 五档行情
        self.bidPrice1 = EMPTY_FLOAT
        self.bidPrice2 = EMPTY_FLOAT
        self.bidPrice3 = EMPTY_FLOAT
        self.bidPrice4 = EMPTY_FLOAT
        self.bidPrice5 = EMPTY_FLOAT

        self.askPrice1 = EMPTY_FLOAT
        self.askPrice2 = EMPTY_FLOAT
        self.askPrice3 = EMPTY_FLOAT
        self.askPrice4 = EMPTY_FLOAT
        self.askPrice5 = EMPTY_FLOAT

        self.bidVolume1 = EMPTY_INT
        self.bidVolume2 = EMPTY_INT
        self.bidVolume3 = EMPTY_INT
        self.bidVolume4 = EMPTY_INT
        self.bidVolume5 = EMPTY_INT

        self.askVolume1 = EMPTY_INT
        self.askVolume2 = EMPTY_INT
        self.askVolume3 = EMPTY_INT
        self.askVolume4 = EMPTY_INT
        self.askVolume5 = EMPTY_INT

    ########################################################################


class SqTradeData(SqBaseData):
    """成交数据类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(SqTradeData, self).__init__()

        # 代码编号相关
        self.symbol = EMPTY_STRING  # 合约代码
        self.exchange = EMPTY_STRING  # 交易所代码
        self.name = EMPTY_STRING  # 代码名称

        self.tradeID = EMPTY_STRING  # 成交编号
        self.vtTradeID = EMPTY_STRING  # 成交在vt系统中的唯一编号，通常是 Gateway名.成交编号

        self.orderID = EMPTY_STRING  # 订单编号
        self.vtOrderID = EMPTY_STRING  # 订单在vt系统中的唯一编号，通常是 Gateway名.订单编号
        self.taskID = EMPTY_STRING
        # 成交相关
        self.direction = EMPTY_UNICODE  # 成交方向
        self.offset = EMPTY_UNICODE  # 成交开平仓
        self.price = EMPTY_FLOAT  # 成交价格
        self.volume = EMPTY_INT  # 成交数量
        self.tradeTime = EMPTY_STRING  # 成交时间


########################################################################
class SqOrderData(SqBaseData):
    """订单数据类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(SqOrderData, self).__init__()

        # 代码编号相关
        self.symbol = EMPTY_STRING  # 合约代码
        self.exchange = EMPTY_STRING  # 交易所代码
        self.name = EMPTY_STRING  # 代码名称

        self.orderID = EMPTY_STRING  # 订单编号
        self.vtOrderID = EMPTY_STRING  # 订单在vt系统中的唯一编号，通常是 Gateway名.订单编号
        self.taskID = EMPTY_STRING

        # 报单相关
        self.direction = EMPTY_UNICODE  # 报单方向
        self.offset = EMPTY_UNICODE  # 报单开平仓
        self.price = EMPTY_FLOAT  # 报单价格
        self.totalVolume = EMPTY_INT  # 报单总数量
        self.tradedVolume = EMPTY_INT  # 报单成交数量
        self.status = EMPTY_UNICODE  # 报单状态

        self.orderTime = EMPTY_STRING  # 发单时间
        self.cancelTime = EMPTY_STRING  # 撤单时间

        # CTP/LTS相关
        self.frontID = EMPTY_INT  # 前置机编号
        self.sessionID = EMPTY_INT  # 连接编号

        self.priceType = EMPTY_STRING
        self.tradePrice = EMPTY_FLOAT


########################################################################
class SqPositionData(SqBaseData):
    """持仓数据类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(SqPositionData, self).__init__()

        # 代码编号相关
        self.symbol = EMPTY_STRING  # 合约代码
        self.exchange = EMPTY_STRING  # 交易所代码
        self.name = EMPTY_STRING  # 代码名称

        # 持仓相关
        self.direction = EMPTY_STRING  # 持仓方向
        self.position = EMPTY_INT  # 持仓量
        self.frozen = EMPTY_INT  # 冻结数量
        self.price = EMPTY_FLOAT  # 持仓均价
        self.vtPositionName = EMPTY_STRING  # 持仓在系统中的唯一代码，symbol.方向

        self.ydPosition = EMPTY_INT  # 昨持仓
        self.tdPosition = EMPTY_INT  # 今持仓

        self.commission = EMPTY_FLOAT
        self.enable = EMPTY_INT
        self.want = EMPTY_INT
        self.initPosition = EMPTY_INT
        self.trading = EMPTY_FLOAT
        self.holding = EMPTY_FLOAT
        self.last = EMPTY_FLOAT
        self.mktval = EMPTY_FLOAT


########################################################################
class SqAccountData(SqBaseData):
    """账户数据类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(SqAccountData, self).__init__()

        # 账号代码相关
        self.accountID = EMPTY_INT  # 账户代码
        self.vtAccountID = EMPTY_STRING  # 账户在vt中的唯一代码，通常是 Gateway名.账户代码
        self.type = EMPTY_STRING

        self.frozen_balance = EMPTY_FLOAT
        self.enable_balance = EMPTY_FLOAT
        self.float_pnl = EMPTY_FLOAT
        self.init_balance = EMPTY_FLOAT
        self.deposit_balance = EMPTY_FLOAT
        self.holding_pnl = EMPTY_FLOAT
        self.close_pnl = EMPTY_FLOAT
        self.margin = EMPTY_FLOAT
        self.trading_pnl = EMPTY_FLOAT
        self.commission = EMPTY_FLOAT


########################################################################
class SqErrorData(SqBaseData):
    """错误数据类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(SqErrorData, self).__init__()

        self.errorID = EMPTY_STRING  # 错误代码
        self.errorMsg = EMPTY_UNICODE  # 错误信息
        self.additionalInfo = EMPTY_UNICODE  # 补充信息

        self.errorTime = time.strftime('%X', time.localtime())  # 错误生成时间


########################################################################
class SqLogData(SqBaseData):
    """日志数据类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(SqLogData, self).__init__()

        self.logTime = time.strftime('%X', time.localtime())  # 日志生成时间
        self.logContent = EMPTY_UNICODE  # 日志信息


########################################################################
class SqContractData(SqBaseData):
    """合约详细信息类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(SqContractData, self).__init__()

        self.exchange = EMPTY_STRING  # 交易所代码
        self.symbol = EMPTY_STRING  # 合约代码
        self.name = EMPTY_UNICODE  # 合约中文名

        self.productClass = EMPTY_UNICODE  # 合约类型
        self.size = EMPTY_INT  # 合约大小
        self.lotsize = EMPTY_INT  # 合约最小交易数量
        self.priceTick = EMPTY_FLOAT  # 合约最小价格TICK

        # 期权相关
        self.strikePrice = EMPTY_FLOAT  # 期权行权价
        self.underlyingSymbol = EMPTY_STRING  # 标的物合约代码
        self.optionType = EMPTY_UNICODE  # 期权类型


########################################################################
class SqSubscribeReq(object):
    """订阅行情时传入的对象类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.symbol = EMPTY_STRING  # 代码
        self.exchange = EMPTY_STRING  # 交易所

        # 以下为IB相关
        self.productClass = EMPTY_UNICODE  # 合约类型
        self.currency = EMPTY_STRING  # 合约货币
        self.expiry = EMPTY_STRING  # 到期日
        self.strikePrice = EMPTY_FLOAT  # 行权价
        self.optionType = EMPTY_UNICODE  # 期权类型


########################################################################
class SqOrderReq(object):
    """发单时传入的对象类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.symbol = EMPTY_STRING  # 代码
        self.exchange = EMPTY_STRING  # 交易所
        self.price = EMPTY_FLOAT  # 价格
        self.volume = EMPTY_INT  # 数量
        self.urgency = EMPTY_INT

        self.priceType = EMPTY_STRING  # 价格类型（'', 'vwap', 'twap')
        self.direction = EMPTY_STRING  # 买卖
        self.offset = EMPTY_STRING  # 开平

        # 以下为IB相关
        self.productClass = EMPTY_UNICODE  # 合约类型
        self.currency = EMPTY_STRING  # 合约货币
        self.expiry = EMPTY_STRING  # 到期日
        self.strikePrice = EMPTY_FLOAT  # 行权价
        self.optionType = EMPTY_UNICODE  # 期权类型


########################################################################
class SqCancelOrderReq(object):
    """撤单时传入的对象类"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.symbol = EMPTY_STRING  # 代码
        self.exchange = EMPTY_STRING  # 交易所

        # 以下字段主要和CTP、LTS类接口相关
        self.orderID = EMPTY_STRING  # 报单号
        self.frontID = EMPTY_STRING  # 前置机号
        self.sessionID = EMPTY_STRING  # 会话号


########################################################################
class SqBasketOrderReq(object):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.positions = []
        self.algo = EMPTY_STRING
        self.params = {}







