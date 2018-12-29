# -*- coding: UTF-8 -*-
import numpy as np
import random
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import Adam



# 全局变量

#批处理个数
BATCH_SIZE = 64

# 奖励折扣率
GAMMA = 0.9

# 贪心度 
EPSILON = 1.0

# 贪心度最小值
EPSILON_MIN = 0.01

# 贪心度折扣率
EPSILON_DECAY = 0.995

# 学习率
LEARNING_RATE = 0.001

# 权重更新比重
TAU = 0.05 


class DQN:
    def __init__(self, env):
        # 传入训练环境env
        self.env = env

        # 初始化参数
        self.memory  = deque(maxlen=2000)  # 记忆队列，最大记忆量为2000
        self.gamma = GAMMA  
        self.epsilon = EPSILON 
        self.epsilon_min = EPSILON_MIN  
        self.epsilon_decay = EPSILON_DECAY  
        self.learning_rate = LEARNING_RATE  
        self.tau = TAU 

        # 创建评估网络 eval_model
        self.eval_model = self.create_model()
        # 创建目标网络 target_model
        self.target_model = self.create_model()

    def create_model(self):

        # 创建深度学习网络模型
        model   = Sequential()

        # 获取输入数据的维度: shape[0]表示行数，shape[1]表示列数
        state_shape  = self.env.states.shape

        # 传入数据，第一层为全连接层，输出节点个数为32
        model.add(Dense(32, input_dim=state_shape[1], activation="relu"))
        model.add(Dropout(0.5))

        # 第二层为全连接层，输出节点个数为64
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.5))

        # 第三层为全连接层，输出个数为32
        model.add(Dense(32, activation="relu"))
        model.add(Dropout(0.5))

        # 第四层为全连接层，输出一个结果，有三种可能值
        model.add(Dense(self.env.n_actions, activation="linear")) # softmax

        # 依据上述设置，创建网络模型
        model.compile(loss="mean_squared_error", optimizer=Adam(lr=self.learning_rate))
        
        return model

    def act(self, state):
        # 更新贪心度值
        self.epsilon *= self.epsilon_decay
        # 在 epsilon 和 epsilon_min 之间，取两者中的较大者为最新的贪心度值

        self.epsilon = max(self.epsilon_min, self.epsilon)
        # 若随机数小于贪心度，进入探索模式，随机选取动作

        if np.random.random() < self.epsilon:
            return np.random.randint(0, self.env.n_actions)
        # 否则按照评估网络 eval_model 预测动作
        return np.argmax(self.eval_model.predict(state)[0])

    def remember(self, state, action, reward, new_state, done):
        # 记忆已训练过的状态数据
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        # 设置批处理数量
        batch_size = BATCH_SIZE
        # 若记忆数据量小于批处理个数
        if len(self.memory) < batch_size: 
            # 直接返回，不进行回放学习
            return
        # 若记忆数据量大于批处理个数，则继续如下回放学习步骤
        # 从记忆序列memory中选择batch_size个随机且独立的元素，用作回放样本
        samples = random.sample(self.memory, batch_size)
        # 遍历随机选出的样本
        for sample in samples:
            # 取出状态数据
            state, action, reward, new_state, done = sample
            # 使用target_model再次预测，预测结果存入target
            target = self.target_model.predict(state)
            # 若取出的是终结状态时的数据
            if done:
                # 直接使用原来的reward 
                target[0][action] = reward
            else:
                # 选取下一个状态中最大的reward，记为Q_future
                Q_future = max(self.target_model.predict(new_state)[0])
                # 使用打折后的Q_future，更新reward
                target[0][action] = reward + Q_future * self.gamma
            # 使用取出的state和更新后的target再次训练评估网络eval_model
            self.eval_model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        # 获取评估网络eval_model的权重参数
        eval_weights = self.eval_model.get_weights()
        # 获取目标网络target_model的权重参数
        target_weights = self.target_model.get_weights()
        # 逐个更新target_model的权重参数
        for i in range(len(target_weights)):
            # 通过tau调节评估网络eval_model和目标网络target_model权重参数的比重，组合起来更新target_model的权重参数
            target_weights[i] = eval_weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        # 设置更新后的权重参数到目标网络target_model
        self.target_model.set_weights(target_weights)
        
    def save_model(self, fn):
        # 保存评估网络eval_model的模型
        self.eval_model.save(fn)

