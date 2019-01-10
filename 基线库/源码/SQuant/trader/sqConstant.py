# -*- coding: UTF-8 -*-
# encoding: UTF-8

from __future__ import unicode_literals
HD_SERVER = 'ipc:///home/xchen/vt_historydata'

########################################################################
#const value
########################################################################
# 默认空值
EMPTY_STRING = ''
EMPTY_UNICODE = u''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0
EMPTY_LONG = 0

# 方向常量
DIRECTION_NONE = u'none'
DIRECTION_LONG = u'long'
DIRECTION_SHORT = u'short'
DIRECTION_UNKNOWN = u'unknown'
DIRECTION_NET = u'net'
DIRECTION_SELL = u'sell'      # IB接口
DIRECTION_COVEREDSHORT = u'covered short'    # 证券期权

# 开平常量
OFFSET_NONE = u'none'
OFFSET_OPEN = u'open'
OFFSET_CLOSE = u'close'
OFFSET_CLOSETODAY = u'close today'
OFFSET_CLOSEYESTERDAY = u'close yesterday'
OFFSET_UNKNOWN = u'unknown'

# 状态常量
STATUS_NOTTRADED = u'pending'
STATUS_PARTTRADED = u'partial filled'
STATUS_ALLTRADED = u'filled'
STATUS_CANCELLED = u'cancelled'
STATUS_REJECTED = u'rejected'
STATUS_UNKNOWN = u'unknown'

# 合约类型常量
PRODUCT_EQUITY = u'股票'
PRODUCT_FUTURES = u'期货'
PRODUCT_BOND = u'债券'
PRODUCT_OPTION = u'期权'
PRODUCT_INDEX = u'指数'
PRODUCT_COMBINATION = u'组合'
PRODUCT_FOREX = u'外汇'
PRODUCT_UNKNOWN = u'未知'
PRODUCT_SPOT = u'现货'
PRODUCT_DEFER = u'延期'
PRODUCT_NONE = ''

# 价格类型常量
PRICETYPE_LIMITPRICE = u'限价'
PRICETYPE_MARKETPRICE = u'市价'
PRICETYPE_FAK = u'FAK'
PRICETYPE_FOK = u'FOK'
PRICETYPE_PRSPLIT = u'PRSPLIT'
PRICETYPE_VWAP = u'VWAP'
PRICETYPE_TWAP = u'TWAP'
PRICETYPE_BESTBIDASK = u'BESTBIDASK'
PRICETYPE_SMARTPRICE = u'SMARTPRICE'

# 期权类型
OPTION_CALL = u'call'
OPTION_PUT = u'put'

# 交易所类型
EXCHANGE_SSE = 'SH'         # 上交所
EXCHANGE_SZSE = 'SZ'        # 深交所
EXCHANGE_CFFEX = 'CFE'      # 中金所
EXCHANGE_SHFE = 'SHF'       # 上期所
EXCHANGE_CZCE = 'CZC'       # 郑商所
EXCHANGE_DCE = 'DCE'        # 大商所
EXCHANGE_CSI = 'CSI'        # 中证指数
EXCHANGE_HKH = 'HKH'        # 沪港通
EXCHANGE_HKS = 'HKS'        # 深港通
EXCHANGE_JZ  = 'JZ'         # 均直
EXCHANGE_SPOT  = 'SPOT'     # 现货
EXCHANGE_IB  = 'IB'         # 银行间市场
EXCHANGE_FX  = 'FX'         # 外汇
EXCHANGE_INE  = 'INE'       # 能源

EXCHANGE_SGE = 'SGE'       # 上金所
EXCHANGE_UNKNOWN = 'UNKNOWN'# 未知交易所
EXCHANGE_NONE = ''          # 空交易所
EXCHANGE_HKEX = 'HKEX'      # 港交所

EXCHANGE_SMART = 'SMART'       # IB智能路由（股票、期权）
EXCHANGE_NYMEX = 'NYMEX'       # IB 期货
EXCHANGE_GLOBEX = 'GLOBEX'     # CME电子交易平台
EXCHANGE_IDEALPRO = 'IDEALPRO' # IB外汇ECN

EXCHANGE_CME = 'CME'           # CME交易所
EXCHANGE_ICE = 'ICE'           # ICE交易所

EXCHANGE_OANDA = 'OANDA'       # OANDA外汇做市商
EXCHANGE_OKCOIN = 'OKCOIN'     # OKCOIN比特币交易所

# 货币类型
CURRENCY_USD = 'USD'            # 美元
CURRENCY_CNY = 'CNY'            # 人民币
CURRENCY_HKD = 'HKD'            # 港币
CURRENCY_UNKNOWN = 'UNKNOWN'    # 未知货币
CURRENCY_NONE = ''              # 空货币

# 数据库
LOG_DB_NAME = 'VnTrader_Log_Db'

# 接口类型
GATEWAYTYPE_EQUITY = 'equity'                   # 股票、ETF、债券
GATEWAYTYPE_FUTURES = 'futures'                 # 期货、期权、贵金属
GATEWAYTYPE_INTERNATIONAL = 'international'     # 外盘
GATEWAYTYPE_BTC = 'btc'                         # 比特币
GATEWAYTYPE_DATA = 'data'                       # 数据（非交易）

########################################################################
#text
########################################################################
SAVE_DATA = 'Save Data'
RESIZE_COLUMNS = 'Resize Columns'

CONTRACT_SYMBOL = 'Symbol'
CONTRACT_NAME = 'Name'
LAST_PRICE = 'Last'
PRE_CLOSE_PRICE = 'PreClose'
VOLUME = 'Volume'
OPEN_INTEREST = 'Open Interest'
OPEN_PRICE = 'Open'
HIGH_PRICE = 'High'
LOW_PRICE = 'Low'
TIME = 'Time'
GATEWAY = 'Gateway'
CONTENT = 'Content'

ERROR_CODE = u'Error Code'
ERROR_MESSAGE = u'Error Message'

TRADE_ID = u'Fill ID'
ORDER_ID = u'Order ID'
DIRECTION = u'Direction'
OFFSET = u'Offset'
PRICE = u'Price'
TRADE_TIME = u'Fill Time'

ORDER_VOLUME = u'Order Volume'
TRADED_VOLUME = u'Filled Volume'
ORDER_STATUS = u'Order Status'
ORDER_TIME = u'Order Time'
CANCEL_TIME = u'Cancel Time'
FRONT_ID = u'Front ID'
SESSION_ID = u'Session ID'
POSITION = u'Position'
YD_POSITION = u'Yesterday Position'
FROZEN = u'Frozen'
POSITION_PROFIT = u'Position Profit'

ACCOUNT_ID = u'Account ID'
PRE_BALANCE = u'Pre Balance'
BALANCE = u'Balance'
AVAILABLE = u'Available'
COMMISSION = u'Commission'
MARGIN = u'Margin'
CLOSE_PROFIT = u'Close Profit'

TRADING = u'Trading'
PRICE_TYPE = u'Price Type'
EXCHANGE = u'Exchange'
CURRENCY = u'Currency'
PRODUCT_CLASS = u'Product Class'
LAST = u'Last'
SEND_ORDER = u'Send Order'
CANCEL_ALL = u'Cancel All'
VT_SYMBOL = u'Vt System Symbol'
CONTRACT_SIZE = u'Contract Size'
PRICE_TICK = u'Price Tick'
STRIKE_PRICE = u'Strike Price'
UNDERLYING_SYMBOL = u'Underlying Symbol'
OPTION_TYPE = u'Option Type'
EXPIRY_DATE = u'Expiry Date'

REFRESH = u'Refresh'
SEARCH = u'Search'
CONTRACT_SEARCH = u'Contract Search'

BID_1 = u'Bid1'
BID_2 = u'Bid2'
BID_3 = u'Bid3'
BID_4 = u'Bid4'
BID_5 = u'Bid5'
ASK_1 = u'Ask1'
ASK_2 = u'Ask2'
ASK_3 = u'Ask3'
ASK_4 = u'Ask4'
ASK_5 = u'Ask5'

BID_PRICE_1 = u'Bid Price 1'
BID_PRICE_2 = u'Bid Price 2'
BID_PRICE_3 = u'Bid Price 3'
BID_PRICE_4 = u'Bid Price 4'
BID_PRICE_5 = u'Bid Price 5'
ASK_PRICE_1 = u'Ask Price 1'
ASK_PRICE_2 = u'Ask Price 2'
ASK_PRICE_3 = u'Ask Price 3'
ASK_PRICE_4 = u'Ask Price 4'
ASK_PRICE_5 = u'Ask Price 5'

BID_VOLUME_1 = u'Bid Volume 1'
BID_VOLUME_2 = u'Bid Volume 2'
BID_VOLUME_3 = u'Bid Volume 3'
BID_VOLUME_4 = u'Bid Volume 4'
BID_VOLUME_5 = u'Bid Volume 5'
ASK_VOLUME_1 = u'Ask Volume 1'
ASK_VOLUME_2 = u'Ask Volume 2'
ASK_VOLUME_3 = u'Ask Volume 3'
ASK_VOLUME_4 = u'Ask Volume 4'
ASK_VOLUME_5 = u'Ask Volume 5'

MARKET_DATA = u'Market Data'
LOG = u'Log'
ERROR = u'Error'
TRADE = u'Fill'
ORDER = u'Order'
POSITION = u'Position'
ACCOUNT = u'Account'
WORKING_ORDER = u'Working Order'

SYSTEM = u'System'
CONNECT_DATABASE = u'Connect Database'
EXIT = u'Exit'
APPLICATION = u'Application'
DATA_RECORDER = u'Data Recorder'
RISK_MANAGER = u'Risk Manager'

STRATEGY = u'Strategy'
CTA_STRATEGY = u'CTA Strategy'

HELP = u'Help'
RESTORE = u'Restore Window'
ABOUT = u'About'
TEST = u'Test'
CONNECT = u'Connect '
EDIT_SETTING = 'Edit Setting'
LOAD = 'Load'
SAVE = 'Save'

CONFIRM_EXIT = u'Confirm Exit？'

GATEWAY_NOT_EXIST = u"Can't find the gateway：{gateway}"
