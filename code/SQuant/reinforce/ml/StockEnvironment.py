# # -*- coding: UTF-8 -*-
# # Author： 施源 Kris
# # Create Time： 2018.8.15
#
# from tensorforce.environments import Environment
# import pandas as pd
# import numpy as np
# import tensorforce
#
# # 全局变量
# # 状态的步长
# N_TIMESTEPS = 5
# # 每次下单交易的股数
# # ORDER_SIZE = 100
#
#
# class StockEnv (Environment):
#     def __init__(self, data,order_size):
#
#         # 获取股价数据，包括过去20天的历史数据和当天(第21天)的开盘价
#         self.xdata = data
#
#         # 初始化环境
#         self.reset(order_size)
#
#     def __str__(self):
#         return 'StockEnvironment'
#
#     def close(self):
#         """
#         Close environment. No other method calls possible afterwards.
#         """
#         print('game over')
#
#     def seed(self, seed):
#         """
#         Sets the random seed of the environment to the given value (current time, if seed=None).
#         Naturally deterministic Environments (e.g. ALE or some gym Envs) don't have to implement this method.
#         Args:
#             seed (int): The seed to use for initializing the pseudo-random number generator (default=epoch time in sec).
#         Returns: The actual seed (int) used OR None if Environment did not override this method (no seeding supported).
#         """
#         return None
#
#     def reset(self,order_size):
#         """
#         Reset environment and setup for new episode.
#         Returns:
#             initial state of reset environment.
#         """
#         # 获取样本个数
#         self.sample_size = len(self.xdata)
#         # 训练次数初始化
#         self.step_counter = 0
#         # 状态步长初始化
#         self.n_timesteps = N_TIMESTEPS
#         # 单笔交易股数初始化
#         self.order_size = order_size
#         # 动作个数初始化
#         self.n_actions = len(self.actions)
#         # 奖励初始化
#         self.reward = 0.
#         # 状态初始化
#         self.current_state = self.states
#         self.next_states = self.xdata[self.step_counter + 1: self.step_counter + self.n_timesteps + 1]
#
#         # 获取交易当天（第21天）的开盘价 —— 用于下单交易
#         self.tradePrice = self.states[-1, 5]
#         # 获取历史（第20天）的收盘价 —— 用于股票价值计量
#         self.cal_value_price = self.states[-1, 3]
#
#         # 当前股票
#         self.stock_amount = 0.  # 持有股票数量初始化
#         self.stock_value = 0.  # 股票价值初始化
#
#         # 当前现金
#         self.cash_hold = 100000.  # 持有现金初始化
#
#         # 当前财富总值初始化 （当前现金+股票价值）
#         self.current_value = self.cash_hold + self.stock_value
#
#         # 过去财富总值初始化
#         self.past_value = 100000.
#
#         # 当前是否为结束状态
#         self.done = False
#
#     def execute(self, action):
#         """
#         Executes action, observes next state(s) and reward.
#         Args:
#             actions: Actions to execute.
#         Returns:
#             Tuple of (next state, bool indicating terminal, reward)
#         """
#         # 更新past_value为最新财富总值
#         self.past_value = self.current_value
#
#         # 用于计算股票价值
#         self.cal_value_price = self.states[-1, 3]
#         #         print(self.cal_value_price)
#         # 用于下单交易
#         self.tradePrice = self.states[-1, 5]
#         #         print(self.tradePrice)
#
#         if action == 1:  # 'buy'
#             # 更新cash总值
#             self.cash_hold = self.cash_hold - self.tradePrice * self.order_size
#             # 更新stock数量
#             self.stock_amount = self.stock_amount + self.order_size
#         elif action == 2:  # 'sell'
#             if self.stock_amount > self.order_size:
#                 # 更新cash总值
#                 self.cash_hold = self.cash_hold + self.tradePrice * self.order_size
#                 # 更新stock数量
#                 self.stock_amount = self.stock_amount - self.order_size
#             else:
#                 action = 0
#                 # elif action == 0: #'hold'
#                 # cash
#         # 这里不考虑现金贬值
#         # 考虑货币的时间价值, 更新现金总值
#         # self.cash_hold = 0.9997 * self.cash_hold
#
#         # 更新state状态
#         # 如果还有下一状态，执行以下操作
#         if self.step_counter + self.n_timesteps + 1 < self.sample_size:
#             self.done = False
#             self.next_states = self.xdata[self.step_counter + 1: self.step_counter + self.n_timesteps + 1]
#             # 获取下一日的收盘价，用于计算股票价值
#             self.stock_value = self.next_states[-1, 3] * self.stock_amount
#             # 更新当天的cash和stock_value
#             self.xdata[self.step_counter + self.n_timesteps, 6] = self.cash_hold
#             self.xdata[self.step_counter + self.n_timesteps, 7] = self.stock_value
#             # 如果没有下一状态，执行以下操作
#         else:
#             self.done = True
#             self.next_states = self.states
#             # 以当日开盘价计算股票价值，因为当天的收盘价在交易中是未知的，只有交易时间结束才能得到
#             self.stock_value = self.next_states[-1, 5] * self.stock_amount
#             # 更新当天的cash和stock_value
#             self.xdata[self.step_counter + self.n_timesteps, 6] = self.cash_hold
#             self.xdata[self.step_counter + self.n_timesteps, 7] = self.stock_value
#
#         # 计算资本总值（现金+股票价值）
#         self.current_value = self.cash_hold + self.stock_value
#         # 奖励规则
#         # 以下情形给予最大惩罚，提前结束：
#         #       1. 现金数量 < 0; 2. 资本总值 < 7万; 3. 手头留存现金不足总资本的30% 4. 卖空操作时，没有足够的现金买回股票
#         if self.cash_hold <= 0 or self.current_value <= 70000. or (
#                     self.cash_hold <= (0.3 * self.current_value)):  # or self.stock_amount < -20
#             self.reward = self.reward - 1.
#
#         if self.stock_amount < 0 and ((-1 * self.stock_amount) > (0.7 * self.cash_hold / self.states[-1, 5])):
#             self.reward = self.reward - 1.
#
#         # 常规的奖励惩罚
#         self.reward = self.reward + 1. * (self.current_value - self.past_value) / self.past_value
#         # self.reward = self.reward + 1. * self.step_counter / (self.sample_size - self.n_timesteps)
#
#         # 更新学习次数
#         self.step_counter = self.step_counter + 1
#
#         return self.next_states, self.done, self.reward
#
#     @property
#     def states(self):
#         """
#         Return the state space. Might include subdicts if multiple states are
#         available simultaneously.
#         Returns:
#             States specification, with the following attributes
#                 (required):
#                 - type: one of 'bool', 'int', 'float' (default: 'float').
#                 - shape: integer, or list/tuple of integers (required).
#         """
#         # 如果当前step_counter，还能往后取20个数据，则返回state
#         if self.step_counter + self.n_timesteps < self.sample_size:
#             states = self.xdata[self.step_counter: self.step_counter + self.n_timesteps]
#             return states
#         # 如果当前step_counter，无法再往后取20个数据，则返回上一个状态的state
#         else:
#             # print("No More Data.")
#             self.done = True
#             states = self.xdata[self.step_counter - 1: self.step_counter + self.n_timesteps - 1]
#             return states
#
#     @property
#     def actions(self):
#         """
#         Return the action space. Might include subdicts if multiple actions are
#         available simultaneously.
#         Returns:
#             actions (spec, or dict of specs): Actions specification, with the following attributes
#                 (required):
#                 - type: one of 'bool', 'int', 'float' (required).
#                 - shape: integer, or list/tuple of integers (default: []).
#                 - num_actions: integer (required if type == 'int').
#                 - min_value and max_value: float (optional if type == 'float', default: none).
#         """
#         # 三种情况: 0 - hold; 1 - buy; 2 - sell
#         actions = [0, 1, 2]
#
#         return actions
#
#     @staticmethod
#     def from_spec(spec, kwargs):
#         """
#         Creates an environment from a specification dict.
#         """
#         env = tensorforce.util.get_object(
#             obj=spec,
#             predefined_objects=tensorforce.environments.environments,
#             kwargs=kwargs
#         )
#         assert isinstance(env, Environment)
#         return env
