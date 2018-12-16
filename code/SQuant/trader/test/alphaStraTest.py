# encoding: utf-8

"""
A very first example of AlphaStrategy back-test:
    Market value weight among UNIVERSE.
    Benchmark is HS300.

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

def save_data():
    """
    This function fetches data from remote server and stores them locally.
    Then we can use local data to do back-test.

    """
    dataview_props = {'start_date': 20180101,  # Start and end date of back-test
                      'end_date': 20181201,
                      'universe': UNIVERSE,  # Investment universe and performance benchmark
                      'benchmark': '000300.SH',
                      'fields': 'total_mv,turnover',  # Data fields that we need
                      'freq': 1  # freq = 1 means we use daily data. Please do not change this.
                      }

    # RemoteDataService communicates with a remote server to fetch data
    ds = RemoteDataService()

    # Use username and password in data_config to login
    ds.init_from_config(data_config)

    # DataView utilizes RemoteDataService to get various data and store them
    dv = DataView()
    dv.init_from_config(dataview_props, ds)
    dv.prepare_data()
    dv.save_dataview(folder_path=dataview_store_folder)


def do_backtest():
    # Load local data file that we just stored.
    dv = DataView()
    dv.load_dataview(folder_path=dataview_store_folder)

    backtest_props = {"start_date": dv.start_date,  # start and end date of back-test
                      "end_date": dv.end_date,
                      "period": "month",  # re-balance period length
                      "benchmark": dv.benchmark,  # benchmark and universe
                      "universe": dv.universe,
                      "init_balance": 1e8,  # Amount of money at the start of back-test
                      "position_ratio": 1.0,  # Amount of money at the start of back-test
                      }
    backtest_props.update(data_config)
    backtest_props.update(trade_config)

    # Create model context using AlphaTradeApi, AlphaStrategy, PortfolioManager and AlphaBacktestInstance.
    # We can store anything, e.g., public variables in context.

    trade_api = AlphaTradeApi()
    strategy = AlphaStrategy(pc_method='market_value_weight')
    pm = PortfolioManager()
    bt = AlphaBacktestInstance()
    context = model.Context(dataview=dv, instance=bt, strategy=strategy, trade_api=trade_api, pm=pm)

    bt.init_from_config(backtest_props)
    bt.run_alpha()

    # After finishing back-test, we save trade results into a folder
    bt.save_results(folder_path=backtest_result_folder)


def analyze_backtest_results():
    # Analyzer help us calculate various trade statistics according to trade results.
    # All the calculation results will be stored as its members.
    ta = ana.AlphaAnalyzer()
    dv = DataView()
    dv.load_dataview(folder_path=dataview_store_folder)

    ta.initialize(dataview=dv, file_folder=backtest_result_folder)

    ta.do_analyze(result_dir=backtest_result_folder,
                  selected_sec=list(ta.universe)[:3])


if __name__ == "__main__":
    save_data()
    do_backtest()
    analyze_backtest_results()