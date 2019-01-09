# -*- encoding: utf-8 -*-

"""
We use user's selection to generate stock selection strategy:
    Market value weight among UNIVERSE.

"""
from __future__ import print_function, unicode_literals, division, absolute_import
import pandas as pd
import numpy as np
import json
import os

from squant.settings import BASE_DIR
from jaqs.data import RemoteDataService
from trader.data import DataView

from trader.trade import model
from trader.trade import (AlphaStrategy, AlphaBacktestInstance,
                        PortfolioManager, AlphaTradeApi)
from trader.straTrading.fieldJudgement import *
import jaqs.trade.analyze as ana

# data_config = {
#     "remote.data.address": "tcp://data.quantos.org:8910",
#     "remote.data.username": "15827606670",
#     "remote.data.password": 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
#                             'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
# }
# trade_config = {
#     "remote.trade.address": "tcp://gw.quantos.org:8901",
#     "remote.trade.username": "15827606670",
#     "remote.trade.password": 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
#                              'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
# }
#
# # Data files are stored in this folder:
# dataview_store_folder = '../../output/simplest/dataview'
#
# # Back-test and analysis results are stored here
# backtest_result_folder = '../../output/simplest'

UNIVERSE = '000807.SH'

dataview_props_example = {'start_date': 20180101,  # Start and end date of back-test
                          'end_date': 20181201,
                          'universe': UNIVERSE,  # Investment universe
                          'benchmark': '000300.SH',  # performance benchmark
                          'fields': 'total_mv,turnover',  # Data fields that we need
                          'freq': 1  # freq = 1 means we use daily data. Please do not change this.
                          }

market_daily_fields = \
            {'open', 'high', 'low', 'close', 'volume', 'turnover', 'vwap', 'oi', 'trade_status',
             'open_adj', 'high_adj', 'low_adj', 'close_adj', 'vwap_adj', 'index_member', 'index_weight'}
reference_daily_fields = \
            {"total_mv", "float_mv", "pe", "pb", "pe_ttm", "pcf_ocf", "pcf_ocfttm", "pcf_ncf",
             "pcf_ncfttm", "ps", "ps_ttm", "turnover_ratio", "free_turnover_ratio", "total_share",
             "float_share", "price_div_dps", "free_share", "np_parent_comp_ttm",
             "np_parent_comp_lyr", "net_assets", "ncf_oper_ttm", "ncf_oper_lyr", "oper_rev_ttm",
             "oper_rev_lyr", "limit_status"}

class AlphaStraGenerator(object):

    def __init__(self, start_date, end_date, universe, benchmark, stock_index, rank_index, period, pc_method, amount,\
                 phone, token, email, strategy_name):
        """

        :param start_date:
        :param end_date:
        :param universe: investment universe
        :param benchmark: performance benchmark
        :param stock_index: 选股指标
        :param rank_index: 排序指标
        :param period: re-balance period length
        :param pc_method: 购股权重
        :param pc_method: 选股数量
        :param phone:  user's trade account
        :param token:
        :param email:  identity of user
        :param strategy_name: 用户输入的策略名
        """
        self.dataview_props = {}
        self.dataview_props['start_date'] = start_date
        self.dataview_props['end_date'] = end_date
        self.dataview_props['universe'] = universe
        self.dataview_props['benchmark'] = benchmark
        self.dataview_props['freq'] = 1

        self.stock_index = stock_index
        self.rank_index = rank_index

        fileds = ""
        index_list = []
        if self.stock_index:
            for index, scope in self.stock_index.iteritems():
                index_list.append(index)
                fileds = fileds + fileds_generator(str(index)) + ","

        if self.rank_index:
            for index, scope in self.rank_index.iteritems():
                if index in index_list:
                    continue
                index_list.append(index)
                fileds = fileds + fileds_generator(str(index)) + ","

        if fileds.endswith(","):
            fileds = fileds[:-1]

        self.dataview_props['fields'] = fileds

        self.period = period  # re-balance period length
        self.pc_method = pc_method  # 购股权重
        self.amount = amount

        self.data_config = {
            "remote.data.address": "tcp://data.quantos.org:8910",
            "remote.data.username": phone,
            "remote.data.password": token
        }
        self.trade_config = {
            "remote.trade.address": "tcp://gw.quantos.org:8901",
            "remote.trade.username": phone,
            "remote.trade.password": token
        }

        # Data files are stored in this folder:
        self.dataview_store_folder = os.path.join(BASE_DIR, "output", email, strategy_name, "dataview").replace('\\', '/')

        # Back-test and analysis results are stored here
        self.backtest_result_folder = os.path.join(BASE_DIR, "output", email, strategy_name).replace('\\', '/')

        # Strategy param storage path
        self.strategy_param_path = os.path.join(BASE_DIR, "output", email, strategy_name + ".json").replace('\\', '/')

        # remote path of report
        self.remote_report_path = os.path.join("http://127.0.0.1:8000", "squant", "output", email, strategy_name, \
                                       "report.html").replace("\\", "/")

    def save_stra(self):
        strategy_param = {}
        strategy_param['dataview_props'] = self.dataview_props
        strategy_param['stock_index'] = self.stock_index
        strategy_param['rank_index'] = self.rank_index
        strategy_param['period'] = self.period
        strategy_param['pc_method'] = self.pc_method

        if not os.path.exists(self.backtest_result_folder):
            os.makedirs(self.backtest_result_folder)

        file = open(self.strategy_param_path, "w+")
        json.dump(strategy_param, file, ensure_ascii=False)
        file.close()

    def save_dataview(self):
        """
        This function fetches data from remote server and stores them locally.
        Then we can use local data to do back-test.

        """
        # RemoteDataService communicates with a remote server to fetch data
        ds = RemoteDataService()

        # Use username and password in data_config to login
        ds.init_from_config(self.data_config)

        # DataView utilizes RemoteDataService to get various data and store them
        dv = DataView()
        dv.init_from_config(self.dataview_props, ds)
        dv.prepare_data()

        if self.stock_index:
            for index, bound in self.stock_index.iteritems():
                if index in market_daily_fields or index in reference_daily_fields:
                    is_quarterly = False
                else:
                    is_quarterly = True
                factor_fomular = index_fomula_generator(str(index), bound[0], bound[1])
                print(factor_fomular)
                fomular_name = index + "_" + "condition"
                dv.add_formula(fomular_name, factor_fomular, is_quarterly=is_quarterly)

        if self.rank_index:
            for index, weight in self.rank_index.iteritems():
                if index in market_daily_fields or index in reference_daily_fields:
                    is_quarterly = False
                else:
                    is_quarterly = True
                factor_fomular = index_fomula_generator(str(index), -1, -1)
                print(factor_fomular)
                fomular_name = str(index) + "_" + "rank"
                dv.add_formula(fomular_name, factor_fomular, is_quarterly=is_quarterly)

        dv.save_dataview(folder_path=self.dataview_store_folder)


    def stock_selector(self, context, user_options=None):
        """
        This function define a selector according to user's selection on stock index

        """
        selector_list = []
        for index, bound in self.stock_index.iteritems():
            fomula_name = index + "_" + "condition"
            selector_list.append(context.snapshot[fomula_name])

        merge = selector_list[0]
        for i in range(1, len(selector_list)):
            tmp = pd.concat([merge, selector_list[i]], axis=1)
            merge = tmp

        result = np.all(merge, axis=1)
        mask = np.all(merge.isnull().values, axis=1)
        result[mask] = False
        return pd.DataFrame(result, index=merge.index)


    def stock_ranker(self, context, useroptions=None):
        """
        This function define a ranker according to user's selection on rank index

        """
        rank_list = []
        weight_list = []
        total_weight = 0
        for index, weight in self.rank_index.iteritems():
            formula_name = index + "_" + "condition"
            rank_list.append(context.snapshot[formula_name])
            weight_list.append(weight)
            total_weight += weight

        rank = pd.DataFrame()
        for i in range(0, len(rank_list)):
            rank['rank_total'] += rank_list[i]*(weight_list[i]/total_weight)

        rank = rank.sort_values('rank_total', ascending=True)
        length = int(rank.shape[0] * 0.2)
        rank.iloc[: length] = 1.0
        rank.iloc[length:] = 0.0
        return rank


    def do_backtest(self):
        # Load local data file that we just stored.
        dv = DataView()
        dv.load_dataview(folder_path=self.dataview_store_folder)
        if "600270.SH" in dv.symbol:
            dv.symbol.remove("600270.SH")

        backtest_props = {"start_date": dv.start_date,  # start and end date of back-test
                          "end_date": dv.end_date,
                          "period": self.period,  # re-balance period length
                          "universe": ','.join(dv.symbol),
                          "benchmark": dv.benchmark,
                          "init_balance": 1e8,  # Amount of money at the start of back-test
                          "position_ratio": 1.0,  # Amount of money at the start of back-test
                          }
        backtest_props.update(self.data_config)
        backtest_props.update(self.trade_config)

        # Create model context using AlphaTradeApi, AlphaStrategy, PortfolioManager and AlphaBacktestInstance.
        # We can store anything, e.g., public variables in context.

        # define user's stock selector
        stock_selector = model.StockSelector()
        stock_selector.add_filter(name="user_selector", func=self.stock_selector)

        # define user's rank method
        stock_rank = model.FactorSignalModel()
        stock_rank.add_signal(name="user_rank_method", func=self.stock_ranker)

        trade_api = AlphaTradeApi()
        if self.stock_index:
            strategy = AlphaStrategy(stock_selector=stock_selector, signal_model=stock_rank, pc_method=self.pc_method)
        else:
            strategy = AlphaStrategy(signal_model=stock_rank, pc_method=self.pc_method)
        pm = PortfolioManager()
        bt = AlphaBacktestInstance()
        context = model.Context(dataview=dv, instance=bt, strategy=strategy, trade_api=trade_api, pm=pm)

        for mdl in [stock_rank, stock_selector]:
            mdl.register_context(context)

        bt.init_from_config(backtest_props)
        bt.run_alpha()

        # After finishing back-test, we save trade results into a folder
        bt.save_results(folder_path=self.backtest_result_folder)

    def analyze_backtest_results(self):
        # Analyzer help us calculate various trade statistics according to trade results.
        # All the calculation results will be stored as its members.
        ta = ana.AlphaAnalyzer()
        dv = DataView()
        dv.load_dataview(folder_path=self.dataview_store_folder)

        ta.initialize(dataview=dv, file_folder=self.backtest_result_folder)

        ta.do_analyze(result_dir=self.backtest_result_folder,
                      selected_sec=list(ta.universe)[:self.amount])


    def run_stra(self):
        # self.save_stra()
        self.save_dataview()
        self.do_backtest()
        self.analyze_backtest_results()


if __name__ == '__main__':
    stock_index = {"turnover_ratio": [-1, 100],
                   "pe": [-1, 20]}
    rank_index = {"oper_rev_ttm": 100, "total_mv": 100, "float_mv": 100, "net_profit_incl_min_int_inc": 100,
                    "ebit": 100, "pe_ttm": 100, "pe": 100, "current_ratio": 100, "quick_ratio": 100, "eps_basic": 100,
                    "pb": 100, "ps_ttm": 100, "pcf_ncfttm": 100, "open": 100, "high": 100, "low": 100, "close": 100,
                    "volume": 100, "turnover_ratio": 100}
    phone = "15827606670"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI" \
            "joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k"
    email = "1"
    # {"start_date": 20181219, "end_date": 20190108, "universe": "000905.SH", "benchmark": "000300.SH", "period": "day",
    #  "pc_method": "equal_weight", "stock_index": {},
    #  "rank_index": {"oper_rev_ttm": 100, "total_mv": 100, "float_mv": 100, "net_profit_incl_min_int_inc": 100,
    #                 "ebit": 100, "pe_ttm": 100, "pe": 100, "current_ratio": 100, "quick_ratio": 100, "eps_basic": 100,
    #                 "pb": 100, "ps_ttm": 100, "pcf_ncfttm": 100, "open": 100, "high": 100, "low": 100, "close": 100,
    #                 "volume": 100, "turnover_ratio": 100}, "amount": 5, "strategy_name": "sort",
    #  "obvious_param": "回测时间：20181219 ~ 20190108, 回测频率：day, 回测基准：000300.SH, 权重：equal_weight, 股数：5, 选股指标：{ }, 排序指标：{ 营业收入(TTM):(100) 总市值:(100) 流通市值:(100) 净利润:(100) 息税前利润:(100) 滚动市盈率:(100) 市盈率:(100) 流动比率:(100) 速动比率:(100) 基本每股收益:(100) 市净率:(100) 市销率(TTM):(100) 市现率:(100) 昨日开盘价:(100) 昨日最高价:(100) 昨日最低价:(100) 昨日收盘价:(100) 昨日成交量:(100) 昨日换手率:(100) }"}

    stra = AlphaStraGenerator(start_date=20181228, end_date=20190109, universe="000905.SH,000300.SH", benchmark="000300.SH",
                              period="day", pc_method="equal_weight", stock_index={}, rank_index={},
                              amount=5, phone=phone, token=token, email=email, strategy_name="sort")
    stra.save_stra()
    stra.run_stra()
    # stra.save_dataview()

    print ("here: run successfully!!!!!!!!!!!!!!!!!!")


