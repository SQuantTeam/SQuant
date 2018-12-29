# -*- coding: UTF-8 -*-
# encoding: UTF-8

from __future__ import print_function
import time

import pandas as pd
from trader.trade.tradeapi import TradeApi

def test_trade_api():
    address = 'tcp://gw.quantos.org:8901'
    username = '15827606670'
    password = 'eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1Mzc4NTM5NDU0NjIiLCJpc3MiOiJhdXRoMCIsImlkIjoiMTU4'\
    'Mjc2MDY2NzAifQ.ODXNTAjCFnD8gAH3NO2hNdv1QjYtTGB-uJLGI3njJ_k'

    tapi = TradeApi(address)

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

    tapi.set_ordstatus_callback(on_orderstatus)
    tapi.set_trade_callback(on_trade)
    tapi.set_task_callback(on_taskstatus)

    # 使用用户名、密码登陆， 如果成功，返回用户可用的策略帐号列表
    user_info, msg = tapi.login(username, password)
    print("1.msg: ", msg)
    # assert check_err_msg(msg)
    print("2.user_info:", user_info)
    user_strats = user_info['strategies']

    # 选择使用的策略帐号
    #
    # 该函数成功后，下单、查持仓等和策略帐号有关的操作都和该策略帐号绑定。
    # 没有必要每次下单、查询都调用该函数。重复调用该函数可以选择新的策略帐号。
    #
    # 如果成功，返回(strategy_id, msg)
    # 否则返回 (0, err_msg)
    if user_strats:
        sid, msg = tapi.use_strategy(user_strats[0])
        assert check_err_msg(msg)
        print('3.sid: ', sid)
        time.sleep(1)

    # 查询Portfolio
    #
    # 返回当前的策略帐号的Universe中所有标的的净持仓，包括持仓为0的标的。

    df, msg = tapi.query_account()
    print('4.', df)
    assert check_err_msg(msg)
    print('5.', df)
    df.to_csv('query_account.csv')

    tapi.close()
    df, msg = tapi.query_account()
    print('4-1.', df)
    assert check_err_msg(msg)
    print('5-1.', df)
    df.to_csv('query_account.csv')


    # 查询当前策略帐号的所有持仓
    #
    # 和 query_portfolio接口不一样。如果莫个期货合约 Long, Short两个方向都有持仓，这里是返回两条记录
    # 返回的 size 不带方向，全部为 正
    df, msg = tapi.query_position()
    assert check_err_msg(msg)
    print('6.', df)
    df.to_csv('query_position.csv')

    # Query Universe
    df_univ, msg = tapi.query_universe()
    df.to_csv('query_universe.csv')

    # 查询Portfolio
    #
    # 返回当前的策略帐号的Universe中所有标的的净持仓，包括持仓为0的标的。

    df_portfolio, msg = tapi.query_portfolio()
    assert check_err_msg(msg)
    print('7.', len(df_univ))
    print(len(df_portfolio))
    # assert len(df_univ) == len(df_portfolio)

    # 下单接口
    #  (task_id, msg) = place_order(code, action, price, size )
    #   action:  Buy, Short, Cover, Sell, CoverToday, CoverYesterday, SellToday, SellYesterday
    # 返回 task_id 可以用改 task_id
    # task_id, msg = tapi.place_order("000718.SZ", "Buy", 3.21, 100)
    # if msg.endswith('market has closed'):
    #     pass
    #     task_id = -1
    # else:
    #     print ('task_msg: ', msg)
    #     # assert check_err_msg(msg)
    # print("task_id:", task_id)
    #
    # df_order, msg = tapi.query_order(task_id=task_id)
    # print ('df_order', df_order)
    # print(df_order)
    #
    # df_trade, msg = tapi.query_trade(task_id=task_id)
    # print('df_trade', df_trade)
    # print(df_trade)

    # 批量下单1：place_batch_order
    #
    # 返回task_id, msg。
    orders = [
        {"security": "600030.SH", "action": "Buy", "price": 16, "size": 1000},
        {"security": "600519.SH", "action": "Buy", "price": 320, "size": 1000},
    ]

    # task_id, msg = tapi.place_batch_order(orders, "", dict())
    # print(task_id)
    # print(msg)

    # cancel_order
    # 撤单
    tapi.cancel_order(task_id='148681126000010')

    # 批量下单2：basket_order
    #
    # 返回task_id, msg。
    orders = [
        {"security": "601857.SH", "ref_price": 8.40, "inc_size": 1000},
        {"security": "601997.SH", "ref_price": 14.540, "inc_size": 20000},
    ]

    task_id, msg = tapi.basket_order(orders, "", {})
    print(task_id)
    print(msg)

    #  goal_protfolio
    #  参数：目标持仓
    #  返回：(result, msg)
    #     result:  成功或失败
    #     msg:     错误原因
    #  注意：目标持仓中必须包括所有的代码的持仓，即使不修改

    # 先查询当前的持仓,
    portfolio, msg = tapi.query_portfolio()
    print("msg:", msg)
    print("portfolio:", portfolio)

    goal = pd.DataFrame(portfolio['current_size'])
    goal.loc[:, 'size'] = goal['current_size']
    goal.loc[:, 'ref_price'] = 0.0
    goal.loc[:, 'urgency'] = 5

    #  然后修改目标持仓
    code = '601857.SH'
    goal.loc[code, 'ref_price'] = 8.38
    goal.loc[code, 'size'] += 20000

    code = '601997.SH'
    goal.loc[code, 'ref_price'] = 14.40
    goal.loc[code, 'size'] += 10000

    # stop_portfolio
    # 撤单, 撤销所有portfolio订单
    #tapi.stop_portfolio()

    # 发送请求
    result, msg = tapi.goal_portfolio(goal)
    print(result, msg)


def check_err_msg(err_msg):
    l = err_msg.split(',')
    return l and (l[0] == '0')


if __name__ == "__main__":
    test_trade_api()