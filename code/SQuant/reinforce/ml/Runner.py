# # -*- coding: UTF-8 -*-
# # Author： 施源 Kris
# # Create Time： 2018.8.15
#
# import DQN
#
# import numpy as np
# import tensorflow as tf
# from keras import backend as K
# from keras.models import load_model
#
# # 全局变量
#
# # 奖励折扣率
# GAMMA = 0.9
#
# # 贪心度
# EPSILON = 1.0
#
# # 贪心度最小值
# EPSILON_MIN = 0.01
#
# # 贪心度折扣率
# EPSILON_DECAY = 0.995
#
#
# class Runner:
#     def __init__(self):
#         # 使用模型之前，添加这两行代码清空之前model占用的内存
#         K.clear_session()
#         tf.reset_default_graph()
#         # 初始化奖励折扣率
#         self.gamma = GAMMA
#         # 初始化贪心度
#         self.epsilon = EPSILON
#         self.epsilon_min = EPSILON_MIN
#         self.epsilon_decay = EPSILON_DECAY
#         # 标志位，用来表示是否训练出收益率较高的成功模型
#         self.train_success = False
#         # runner运行结束后，需要返回最终训练出的模型的名字，以便测试
#         self.model_name = ''
#
#     def trainer(self, symbol, env, epochs,order_size):
#         # 获取环境
#         self.env = env
#         # 初始化dqn_agent
#         self.dqn_agent = DQN.DQN(env=self.env)
#         # 初始化执行轮次
#         self.epochs = epochs
#         # 初始化每轮次的训练步数
#         self.epoch_len = self.env.sample_size - self.env.n_timesteps
#
#         # 开始执行epochs轮次的训练
#         for epoch in range(self.epochs):
#             # 初始化训练环境
#             self.env.reset(order_size)
#             # 获取当前状态
#             cur_state = self.env.states
#             # 初始化资本总值记录
#             fortune = list()
#             # 初始化持有现金
#             cash = list()
#             # 初始化动作记录
#             act = list()
#             # 初始化奖励记录
#             re = list()
#             # 开始本轮的训练
#             for step in range(self.epoch_len):
#                 # 根据当前状态选择action
#                 action = self.dqn_agent.act(cur_state)
#                 # 执行action，返回环境中的下一个状态
#                 new_state, done, reward = self.env.execute(action)
#                 # 记录当前采取的行动，添加到action记录表
#                 act.append(action)
#                 # 记录当前返回的奖励，添加到reward记录表
#                 re.append(reward)
#                 # 记录当前持有的现金，添加到cash记录表
#                 cash.append(new_state[-1, 6])
#                 # 计算当前状态的资本总值，添加到fortune记录表
#                 _fortune = new_state[-1, 6] + new_state[-1, 7]
#                 fortune.append(_fortune)
#
#                 # 存入回放记忆
#                 self.dqn_agent.remember(cur_state, action, reward, new_state, done)
#                 # 经验回放
#                 self.dqn_agent.replay()
#                 if step > 20:
#                     # 更新模型参数
#                     self.dqn_agent.target_train()
#                     # 获取下一个状态
#                 cur_state = new_state
#
#                 # 若为结束状态，跳出循环；否则继续训练
#                 if done:
#                     profit_ratio_str = (fortune[-1] / fortune[0]).__format__(".2f")
#                     # 训练出成功模型，保存前缀名为success的模型
#                     if fortune[-1] >= 102000. and cash[-1] >= 0.:
#                         self.train_success = True
#                         self.model_name = "success-model-{}-{}.h5".format(symbol, profit_ratio_str)
#                         self.dqn_agent.save_model(self.model_name)
#                     # 训练未成功，保存前缀名为train的模型
#                     else:
#                         self.train_success = False
#                         self.model_name = "train-model-{}-{}.h5".format(symbol, profit_ratio_str)
#                         self.dqn_agent.save_model(self.model_name)
#                     break
#
#             print("Epoch {}: Fortune-{}, Cash-{}, Reward-{}".format(str(epoch), fortune[-1], cash[-1], re[-1]))
#             # # 输出训练的最终资本总值
#             # print("Fortune for epoch " + str(epoch) + " : ")
#             # print(fortune[-1])
#             # # 输出本轮次所有行为
#             # print("Actions for epoch " + str(epoch) + ":")
#             # print(act)
#             # # 输出本轮次所有奖励
#             # print("Rewards for epoch "+ str(epoch) + ":")
#             # print(re)
#             # # 输出本轮次所有现金
#             # print("Cash for epoch " + str(epoch) + ":")
#             # print(cash)
#
#         # 完成所有轮次训练后，返回训练后的模型名称
#         return self.model_name
#
#     def tester(self, env, model_name,order_size):
#         # 根据测试数据，初始化环境
#         self.env = env
#         # 初始化每轮次的训练步数
#         self.epoch_len = self.env.sample_size - self.env.n_timesteps
#         # # 初始化model_name
#         self.model_name = model_name
#         # 根据模型名称，载入模型
#         self.test_model = load_model(self.model_name)
#
#         # 初始化测试环境
#         self.env.reset(order_size)
#         # 获取当前状态
#         cur_state = self.env.states
#         # 初始化资本总值记录
#         fortune = list()
#         # 初始化持有现金
#         cash = list()
#         # 初始化动作记录
#         act = list()
#         # 初始化奖励记录
#         re = list()
#         # 开始测试
#         for step in range(self.epoch_len):
#             # # 使用现有模型，根据当前状态选择action
#             # action = np.argmax(self.test_model.predict(cur_state)[0])
#
#             # 更新贪心度值
#             self.epsilon *= self.epsilon_decay
#             # 在 epsilon 和 epsilon_min 之间，取两者中的较大者为最新的贪心度值
#             self.epsilon = max(self.epsilon_min, self.epsilon)
#             # 若随机数小于贪心度，进入探索模式，随机选取动作
#             if np.random.random() < self.epsilon:
#                 action = np.random.randint(0, self.env.n_actions)
#             # 否则按照评估网络 test_model 预测动作
#             else:
#                 action = np.argmax(self.test_model.predict(cur_state)[0])
#
#             # 执行action，返回环境中的下一个状态
#             new_state, done, reward = self.env.execute(action)
#
#             # 记录当前采取的行动，添加到action记录表
#             act.append(action)
#             # 记录当前返回的奖励，添加到reward记录表
#             re.append(reward)
#             # 记录当前持有的现金，添加到cash记录表
#             cash.append(new_state[-1, 6])
#             # 计算当前状态的资本总值，添加到fortune记录表
#             _fortune = new_state[-1, 6] + new_state[-1, 7]
#             fortune.append(_fortune)
#
#             # 获取下一个状态
#             cur_state = new_state
#
#             # 若为结束状态，跳出循环；否则继续训练
#             if done:
#                 break
#
#         print("Test Result: Fortune-{}, Cash-{}, Reward-{}".format(fortune[-1], cash[-1], re[-1]))
#         # # 输出测试的最终资本总值
#         # print("Test Fortune :")
#         # print(fortune[-1])
#         # # 输出测试的所有行为
#         # print("Test Actions :")
#         # print(act)
#         # # 输出测试的所有奖励
#         # print("Test Rewards :")
#         # print(re)
#         # # 输出测试的所有现金
#         # print("Test Cash :")
#         # print(cash)
#
#         # 返回结果，用于画图
#         return fortune, act, re, cash
