# -*- coding: UTF-8 -*-
# encoding: UTF-8
"""
PortfolioManager helps manage strategy's trades, orders, positions, etc.

It binds with a strategy and updates trades/orders/positions when relevant callback
functions are called.

"""

from __future__ import print_function

import copy

import trader.trade
from trader.data.basic import OrderStatusInd, Trade, Task, Order, Position, TradeStat
from trader.trade import common


class PortfolioManager(object):
    """
    Used to store relevant context of the strategy.
    """

    # TODO want / frozen update
    def __init__(self):
        self.ctx = None

        self.orders = dict()
        self.tasks = dict()
        self.trades = []
        self._cum_net_turnover = 0.0
        self.cash = 0.0
        self.init_balance = 0.0

        self.positions = dict()
        self.tradestat = dict()

        self.holding_securities = set()

    def init_from_config(self, props):
        self.init_balance = props.get("init_balance", 0.0)
        self.cash = self.init_balance

        self._hook_strategy()

    def _hook_strategy(self):
        self.original_on_order_status = self.ctx.strategy.on_order_status
        self.ctx.strategy.on_order_status = self._on_order_status

        self.original_on_trade = self.ctx.strategy.on_trade
        self.ctx.strategy.on_trade = self._on_trade

        self.original_on_order_rsp = self.ctx.strategy.on_order_rsp
        self.ctx.strategy.on_order_rsp = self._on_order_rsp

        # self.original_on_task_rsp = self.ctx.strategy.on_task_rsp
        # self.ctx.strategy.on_task_rsp = self._on_task_rsp

    @staticmethod
    def _make_position_key(symbol):
        # return '@'.join(symbol)
        return symbol

    @staticmethod
    def _make_order_key(entrust_id, trade_date):
        return '@'.join((str(entrust_id), str(trade_date)))

    def _on_order_rsp(self, rsp):
        self.original_on_order_rsp(rsp)

    def _make_trade_stat_key(self, symbol):
        # return '@'.join(symbol)
        return '{:s}@{}'.format(symbol, self.ctx.trade_date)

    def _get_trade_stat(self, symbol):
        """

        Parameters
        ----------
        symbol : str

        Returns
        -------
        TradeStat

        """
        key = self._make_trade_stat_key(symbol)
        trade_stat = self.tradestat.get(key, None)
        if trade_stat is None:
            trade_stat = TradeStat(symbol=symbol)
        return trade_stat

    def get_trade_stat(self, symbol):
        """

        Parameters
        ----------
        symbol : str

        Returns
        -------
        TradeStat

        """
        key = self._make_trade_stat_key(symbol)
        trade_stat = self.tradestat.get(key, None)
        return trade_stat

    def get_position(self, symbol):
        pos_key = self._make_position_key(symbol)
        position = self.positions.get(pos_key, None)
        return position

    def get_pos(self, symbol):
        pos_key = self._make_position_key(symbol)
        position = self.positions.get(pos_key, None)
        if position is None:
            return 0
        else:
            return position.current_size

    def get_task(self, task_id):
        """

        Parameters
        ----------
        task_id : int

        Returns
        -------
        Task

        """
        return self.tasks.get(task_id, None)

    def init_positions(self):
        df_acc, msg = self.ctx.trade_api.query_account()
        if not msg.split(',')[0] == '0':
            print(msg)
            raise RuntimeError("Query account failed")
        account_info = df_acc.set_index('type').to_dict(orient='index')

        df_univ, msg = self.ctx.trade_api.query_universe()
        df_univ = df_univ.rename(columns={'security': 'symbol'})
        univ = df_univ['symbol'].values.copy()
        # self.ctx.init_universe(univ)

        df_pos, msg = self.ctx.trade_api.query_position()
        df_pos = df_pos.rename(columns={'security': 'symbol'})
        pos_list = Position.create_from_df(df_pos)
        pos_dic = {p.symbol: p for p in pos_list}
        self.positions.update(pos_dic)

    # ----------------------------------------------------------------------------
    # On Task Change

    def add_task(self, task):
        """
        Add order to orders, create position and tradestat if necessary.

        Parameters
        ----------
        task : Task

        """
        if task.task_id in self.tasks:
            print('duplicate task {}'.format(task.task_id))

        # Store Task (right after strategy constructs a task)
        # TODO: copy
        self.tasks[task.task_id] = copy.deepcopy(task)

        # Store/Update TradeStat (right after strategy constructs a task)
        if task.function_name == 'place_order':
            order = task.data
            # self.orders[order.entrust_no] = order
            self._update_trade_stat_from_order(order)

        elif task.function_name == 'place_batch_order':
            orders = task.data
            for order in orders:
                # self.orders[order.entrust_no] = order
                self._update_trade_stat_from_order(order)

        elif task.function_name == 'basket_order':
            # TODO: no Order class for basket_order
            raise NotImplementedError("basket_order")

        elif task.function_name == 'goal_portfolio':
            # self._update_trade_stat_from_goal_positions(goal_positions)
            # orders = task.data
            for entrust_no, order in task.data.items():
                self._update_trade_stat_from_order(order)


    def _update_trade_stat_from_order(self, order, roll_back=False):
        """

        Parameters
        ----------
        order : Order
            Not yet filled.
        roll_back : bool
            if the order is canceled, or task is failed/stopped, we roll back our previous change.

        """
        sign = 1
        if roll_back:
            sign *= -1

        tradestat = self._get_trade_stat(order.symbol)

        # if order.entrust_action == common.ORDER_ACTION.BUY:
        if common.ORDER_ACTION.is_positive(order.entrust_action):
            tradestat.buy_want_size += order.entrust_size * sign
        else:
            tradestat.sell_want_size += order.entrust_size * sign

        self.tradestat[self._make_trade_stat_key(order.symbol)] = tradestat

    def _update_trade_stat_from_goal_positions(self, positions, roll_back=False):
        """

        Parameters
        ----------
        positions : list of dict
            [ {"security": "000001.SZ", "ref_price": 10.0, "size" : 100}, ...]
        roll_back : bool
            if the order is canceled, or task is failed/stopped, we roll back our previous change.

        """
        sign = 1
        if roll_back:
            sign *= -1

        for goal_pos in positions:
            size = goal_pos['size']
            if size == 0:
                continue
            symbol = goal_pos['symbol']

            tradestat = self._get_trade_stat(symbol)

            # tradestat.buy_want_size = 0
            # tradestat.sell_want_size = 0
            if size > 0:
                tradestat.buy_want_size += size * sign
            else:
                tradestat.sell_want_size += size * sign

            self.tradestat[self._make_trade_stat_key(symbol)] = tradestat


    # ----------------------------------------------------------------------------
    # On Order Status

    def _update_task_if_done(self, task_id):
        task = self.get_task(task_id)
        if task is None:
            return
        if task.function_name == 'place_order':
            order = task.data
            if order.is_finished:
                task.task_status = common.TASK_STATUS.DONE
        elif task.function_name == 'place_batch_order':
            orders = task.data
            # if all([o.is_finished for o in orders]):
            has_unfinished = False
            for o in orders:
                if not o.is_finished:
                    has_unfinished = True
                    break
            if not has_unfinished:
                task.task_status = common.TASK_STATUS.DONE
        elif task.function_name == 'goal_portfolio':
            orders = task.data
            # if all([o.is_finished for o in orders]):
            has_unfinished = False
            for entrust_no, o in orders.items():
                if not o.is_finished:
                    has_unfinished = True
                    break
            if not has_unfinished:
                task.task_status = common.TASK_STATUS.DONE
        else:
            raise NotImplementedError()

        self.tasks[task_id] = task

    def _on_order_status(self, ind):
        """

        Parameters
        ----------
        ind : OrderStatusInd

        """

        if ind.task_id not in self.tasks:
            return

        # TODO
        if ind.entrust_no == 101010 or ind.entrust_no == 202020:  # trades generate by system
            return

        # add/update order
        order = self.orders.get(ind.entrust_no, None)
        if order is None:
            order = Order()
            self.orders[ind.entrust_no] = order
        order.copy(ind)

        task = self.get_task(ind.task_id)
        if task.function_name == 'place_order':
            order = task.data
            order.copy(ind)
        elif task.function_name == 'place_batch_order':
            for order in task.data:
                if order.entrust_no == ind.entrust_no:
                    order.copy(ind)
        elif task.function_name == 'goal_portfolio':
            # for order in task.data:
            #    if order.entrust_no == ind.entrust_no:
            if ind.entrust_no in task.data:
                order = task.data[ind.entrust_no]
                order.copy(ind)

        # order status other than CANCELLED/REJECTED will be dealt with self.on_trade
        if (ind.order_status == common.ORDER_STATUS.CANCELLED) or (ind.order_status == common.ORDER_STATUS.REJECTED):

            # update TradeStat
            trade_stat = self._get_trade_stat(ind.symbol)

            release_size = ind.entrust_size - ind.fill_size
            if common.ORDER_ACTION.is_positive(ind.entrust_action):
                trade_stat.buy_want_size -= release_size
            else:
                trade_stat.sell_want_size -= release_size

            self.tradestat[self._make_trade_stat_key(ind.symbol)] = trade_stat

            # update task
            self._update_task_if_done(ind.task_id)

        self.original_on_order_status(ind)



    # ----------------------------------------------------------------------------
    # On Trade Indication

    def _on_trade(self, ind):
        # record trades
        self.trades.append(ind)

        # Change Position
        self._update_position_by_trade_ind(ind)

        # Update cash
        self._update_cash_from_trade_ind(ind)

        # Change TradeStat
        self._update_trade_stat_from_trade_ind(ind)

        # Update Orders
        # self._update_order_from_trade_ind(ind)

        # Update Tasks
        if not (ind.entrust_no == 101010 or ind.entrust_no == 202020):  # trades generate by system
            self._update_task_if_done(ind.task_id)

        # hook:
        self.original_on_trade(ind)

    def _update_cash_from_trade_ind(self, ind):
        """

        Parameters
        ----------
        ind : Trade

        """
        curr_pos = self.get_pos(ind.symbol)
        turnover = ind.fill_price * ind.fill_size
        if common.ORDER_ACTION.is_positive(ind.entrust_action):
            self._cum_net_turnover += turnover
        else:
            self._cum_net_turnover -= turnover
        self.cash = self.init_balance - (self._cum_net_turnover - curr_pos * ind.fill_price)

        # TODO
        if self.cash < 0:
            pass
            # print("WARNING: cash is not enough when executing trade\n", ind)

    def _update_order_from_trade_ind(self, ind):
        order = self.orders.get(ind.entrust_no)
        if order is None:
            return

        order.fill_size += ind.fill_size

        task = self.get_task(ind.task_id)
        if task.function_name == 'place_order':
            order = task.data
            order.fill_size += ind.fill_size
        elif task.function_name == 'place_batch_order':
            for order in task.data:
                order.fill_size += ind.fill_size
        else:
            raise NotImplementedError()

    def _update_trade_stat_from_trade_ind(self, ind):
        """

        Parameters
        ----------
        ind : Trade
            Not yet filled.

        """
        tradestat = self._get_trade_stat(ind.symbol)

        if common.ORDER_ACTION.is_positive(ind.entrust_action):
            tradestat.buy_filled_size += ind.fill_size
            tradestat.buy_want_size -= ind.fill_size
        elif common.ORDER_ACTION.is_negative(ind.entrust_action):
            tradestat.sell_filled_size += ind.fill_size
            tradestat.sell_want_size -= ind.fill_size

        self.tradestat[self._make_trade_stat_key(ind.symbol)] = tradestat

    def _update_position_by_trade_ind(self, ind):
        # ignore no fill_size (which should not be)
        if ind.fill_size == 0:
            print("WARNING: no fill_size TradeInd found!")
            return

        # get position, if no, create a new one.
        pos_key = self._make_position_key(ind.symbol)
        pos = self.positions.get(pos_key, None)
        if pos is None:
            pos = Position(symbol=ind.symbol)

        if common.ORDER_ACTION.is_positive(ind.entrust_action):
            pos.current_size += ind.fill_size
        elif common.ORDER_ACTION.is_negative(ind.entrust_action):
            pos.current_size -= ind.fill_size

        self.positions[pos_key] = pos

        # if no holding, remove the position from the dict
        if pos.current_size == 0:
            self.positions.pop(pos_key)
            # TODO : remove holding_securities field
            self.holding_securities.remove(ind.symbol)
        else:
            self.holding_securities.add(ind.symbol)

    # ----------------------------------------------------------------------------
    # For Alpha Strategy

    def market_value(self, ref_prices, suspensions=None):
        """
        Calculate total market value according to all current positions.
        NOTE for now this func only support stocks.

        Parameters
        ----------
        ref_prices : dict of {symbol: price}
            The prices we refer to to get symbol price.
        suspensions : list of securities
            Securities that are suspended.

        Returns
        -------
        market_value : float

        """
        if suspensions is None:
            suspensions = []

        market_value_float = 0.0
        market_value_frozen = 0.0  # suspended or high/low limit
        for sec in self.holding_securities:
            size = self.get_position(sec).current_size
            # TODO PortfolioManager object should not access price
            price = ref_prices[sec]
            mv_sec = price * size
            if sec in suspensions:
                market_value_frozen += mv_sec
            else:
                market_value_float += mv_sec

        return market_value_float, market_value_frozen

