# -*- coding: utf-8 -*-
from trader.sqConstant import *
# 行情地址
MdAddress = 'tcp://data.quantos.org:8910'
# 交易地址
TdAddress = 'tcp://gw.quantos.org:8901'

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
statusMapReverse['Rejected'] = STATUS_REJECTED
statusMapReverse['Rejected'] = STATUS_REJECTED
statusMapReverse['Rejected'] = STATUS_REJECTED