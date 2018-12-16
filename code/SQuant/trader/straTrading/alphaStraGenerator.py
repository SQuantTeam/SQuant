# encoding: utf-8

"""
We use user's selection to generate stock selection strategy:
    Market value weight among UNIVERSE.
    Benchmark is HS300(沪深300).

"""
from __future__ import print_function, unicode_literals, division, absolute_import

from jaqs.data import RemoteDataService, DataView

from trader.trade import model
from trader.trade import (AlphaStrategy, AlphaBacktestInstance,
                        PortfolioManager, AlphaTradeApi)
import jaqs.trade.analyze as ana

data_config = {
    "remote.data.address": "tcp://data.quantos.org:8910",
    "remote.data.username": "15827606670",
    "remote.data.password": 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
                            'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
}
trade_config = {
    "remote.trade.address": "tcp://gw.quantos.org:8901",
    "remote.trade.username": "15827606670",
    "remote.trade.password": 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkI' \
                             'joiMTU4Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'
}

# Data files are stored in this folder:
dataview_store_folder = '../../output/simplest/dataview'

# Back-test and analysis results are stored here
backtest_result_folder = '../../output/simplest'

UNIVERSE = '000807.SH'

dataview_props_example = {'start_date': 20180101,  # Start and end date of back-test
                          'end_date': 20181201,
                          'universe': UNIVERSE,  # Investment universe
                          'benchmark': '000300.SH',  # performance benchmark
                          'fields': 'total_mv,turnover',  # Data fields that we need
                          'freq': 1  # freq = 1 means we use daily data. Please do not change this.
                          }

class AlphaStraGenerator(object):

    def __init__(self, start_date, end_date, universe, benchmark, stock_index, rank_index, period, pc_method):
        self.dataview_props = {}
        self.dataview_props['start_date'] = start_date
        self.dataview_props['end_date'] = end_date
        self.dataview_props['universe'] = universe
        self.dataview_props['benchmark'] = benchmark
        self.dataview_props['freq'] = 1
        self.dataview_props['fileds'] = None # To do

        self.stock_index = stock_index
        self.rank_index = rank_index
        self.period = period
        self.pc_method = pc_method


    def save_dataview(self):
        """
        This function fetches data from remote server and stores them locally.
        Then we can use local data to do back-test.

        """
        # RemoteDataService communicates with a remote server to fetch data
        ds = RemoteDataService()

        # Use username and password in data_config to login
        ds.init_from_config(data_config)

        # DataView utilizes RemoteDataService to get various data and store them
        dv = DataView()
        dv.init_from_config(self.dataview_props, ds)
        dv.prepare_data()
        dv.save_dataview(folder_path=dataview_store_folder)


    def stock_selector(self, context, user_options=None):
        """
        This function define a selector according to user's selection on stock index

        """
        selector_list = []
        for index in self.stock_index:
            selector_list.append(context.snapshot[index])
        

        return

    def stock_rank(self, context, useroptions=None):
        """
        This function define a ranker according to user's selection on rank index

        """
        rank_list = []
        for index in self.rank_index:
            rank_list.append(context.snapshot[index])

        return


    def do_backtest(self):
        # Load local data file that we just stored.
        dv = DataView()
        dv.load_dataview(folder_path=dataview_store_folder)

        backtest_props = {"start_date": dv.start_date,  # start and end date of back-test
                          "end_date": dv.end_date,
                          "period": self.period,  # re-balance period length
                          "benchmark": dv.benchmark,  # benchmark and universe
                          "universe": dv.universe,
                          "init_balance": 1e8,  # Amount of money at the start of back-test
                          "position_ratio": 1.0,  # Amount of money at the start of back-test
                          }
        backtest_props.update(data_config)
        backtest_props.update(trade_config)

        # Create model context using AlphaTradeApi, AlphaStrategy, PortfolioManager and AlphaBacktestInstance.
        # We can store anything, e.g., public variables in context.

        # define user's stock selector
        stock_selector = model.StockSelector()
        stock_selector.add_filter(name="user_selector", func=self.stock_selector)

        # define user's rank method
        stock_rank = model.FactorSignalModel()
        stock_rank.add_signal(name="user_rank_method", func=self.stock_rank)

        trade_api = AlphaTradeApi()
        strategy = AlphaStrategy(stock_selector=stock_selector, signal_model=stock_rank, pc_method=self.pc_method)
        pm = PortfolioManager()
        bt = AlphaBacktestInstance()
        context = model.Context(dataview=dv, instance=bt, strategy=strategy, trade_api=trade_api, pm=pm)

        bt.init_from_config(backtest_props)
        bt.run_alpha()

        # After finishing back-test, we save trade results into a folder
        bt.save_results(folder_path=backtest_result_folder)

    def analyze_backtest_results(self):
        # Analyzer help us calculate various trade statistics according to trade results.
        # All the calculation results will be stored as its members.
        ta = ana.AlphaAnalyzer()
        dv = DataView()
        dv.load_dataview(folder_path=dataview_store_folder)

        ta.initialize(dataview=dv, file_folder=backtest_result_folder)

        ta.do_analyze(result_dir=backtest_result_folder,
                      selected_sec=list(ta.universe)[:3])


    def run_stra(self):
        self.save_dataview()
        self.do_backtest()
        self.analyze_backtest_results()

if __name__ == '__main':
    stra = AlphaStraGenerator()
    stra.run_stra()

