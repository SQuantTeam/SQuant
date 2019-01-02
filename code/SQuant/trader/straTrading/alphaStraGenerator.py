# -*- coding: UTF-8 -*-
# encoding: utf-8

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
from jaqs.data import RemoteDataService, DataView

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
                fileds = fileds + fileds_generator(index) + ","

        if self.rank_index:
            for index, scope in self.rank_index.iteritems():
                if index in index_list:
                    continue
                index_list.append(index)
                fileds = fileds + fileds_generator(index) + ","

        if fileds.endswith(","):
            fileds = fileds[:-1]

        self.dataview_props['fileds'] = fileds

        print("数据区域: " , self.dataview_props['fileds'])

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
        print(self.dataview_props)
        dv.init_from_config(self.dataview_props, ds)
        dv.prepare_data()

        for index, bound in self.stock_index.iteritems():
            factor_fomular = index_fomula_generator(index, bound[0], bound[1])
            print(factor_fomular)
            fomular_name = index + "condition"
            dv.add_formula(fomular_name, factor_fomular, is_quarterly=False)

        for index, weight in self.rank_index.iteritems():
            factor_fomular = index_fomula_generator(index, -1, -1)
            print(factor_fomular)
            fomular_name = index
            dv.add_formula(fomular_name, factor_fomular, is_quarterly=False)   # todo: is_quarterly judgement

        dv.save_dataview(folder_path=self.dataview_store_folder)


    def stock_selector(self, context, user_options=None):
        """
        This function define a selector according to user's selection on stock index

        """
        selector_list = []
        for index, bound in self.stock_index.iteritems():
            selector_list.append(context.snapshot[index])

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
            rank_list.append(context.snapshot[index])
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
        strategy = AlphaStrategy(stock_selector=stock_selector, signal_model=stock_rank, pc_method=self.pc_method)
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
    stock_index = {"pb": [-1, 2],
                   "pe": [-1, 20]}
    rank_index = {"pb": 1,
                  "pe": 1}
    phone = "15827606670"
    token = "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI" \
            "joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k"
    email = "1"
    stra = AlphaStraGenerator(start_date=20180101, end_date=20181201, universe="000905.SH,000300.SH", benchmark="000300.SH",
                              period="week", pc_method="equal_weight", stock_index=stock_index, rank_index =rank_index,
                              amount=5, phone=phone, token=token, email=email, strategy_name="test")
    stra.save_stra()
    stra.run_stra()


