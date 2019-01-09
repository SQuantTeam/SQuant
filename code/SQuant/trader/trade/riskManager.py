# encoding: UTF-8

from __future__ import division

import json
import os
import platform

from trader.sqConstant import *


########################################################################
class RiskManager(object):
    """风控引擎"""

    name = u'风控模块'

    # ----------------------------------------------------------------------
    def __init__(self, active, order_size_limit, order_price_upper_limit, balance_use_limit, trade_limit, trade_count):
        """Constructor"""

        self.active = active

        # 单笔委托相关
        self.order_size_limit = int(order_size_limit)  # 单笔委托最大限制
        self.order_price_upper_limit = float(order_price_upper_limit)  # 单笔委托价格相对于行情的最大比率
        self.balance_use_limit = float(balance_use_limit)  # 单笔下单金额占账户可用资金最大比率

        # 成交统计相关
        self.trade_count = trade_count  # 当日成交合约数量统计
        self.trade_limit = int(trade_limit)  # 当日成交合约数量限制


    # # ----------------------------------------------------------------------
    # def loadSetting(self):
    #     """读取配置"""
    #     with open(self.setting_file_path) as f:
    #         d = json.load(f)
    #
    #         # 设置风控参数
    #         self.order_size_limit = d['order_size_limit']
    #         self.order_price_upper_limit = d['order_price_upper_limit']
    #         self.trade_limit = d['trade_limit']
    #         self.balance_use_limit = d['balance_use_limit']
    #
    # # ----------------------------------------------------------------------
    # def saveSetting(self):
    #     """保存风控参数"""
    #     with open(self.setting_file_path, 'w') as f:
    #         # 保存风控参数
    #         d = {}
    #
    #         d['order_size_limit'] = self.order_size_limit
    #         d['order_price_upper_limit'] = self.order_price_upper_limit
    #         d['trade_limit'] = self.trade_limit
    #         d['balance_use_limit'] = self.balance_use_limit
    #
    #         # 写入json
    #         jsonD = json.dumps(d, indent=4)
    #         f.write(jsonD)

    # ----------------------------------------------------------------------
    def checkRisk(self, orderReq, tick, account):
        """检查风险"""
        # 如果没有启动风控检查，则直接返回成功
        msg = ""
        if not self.active:
            msg = u"风控: 风控引擎未开启"
            return msg, True

        # 检查委托数量
        if orderReq.volume <= 0:
            msg = u"风控: 无效的订单数量"
            return msg, False

        if orderReq.volume > self.order_size_limit:
            msg = (u'风控：单笔委托数量%s，超过限制%s'
                              % (orderReq.volume, self.order_size_limit))
            return msg, False

        if orderReq.price / tick.lastPrice > self.order_price_upper_limit:
            msg = (u'风控：委托价格%s，超过限制比率%s'
                              % (orderReq.price, self.order_price_upper_limit))
            return msg, False

        # 检查成交合约量
        if self.trade_count >= self.trade_limit:
            msg = (u'风控：今日总成交合约数量%s，超过限制%s'
                              % (self.trade_count, self.trade_limit))
            return msg, False

        if orderReq.price * orderReq.volume / account.enable_balance > self.balance_use_limit:
            msg = (u'风控：委托成交额超过账户可用余额比例限制%s'
                              % (self.balance_use_limit))
            return msg, False

        msg = u"风控：通过风控"
        return msg, True

    # # ----------------------------------------------------------------------
    # def stop(self):
    #     """停止"""
    #     self.saveSetting()

