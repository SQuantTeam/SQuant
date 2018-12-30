# -*- coding: UTF-8 -*-
# 导入基础模块
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

# 导入 pyqt5 相关模块
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QPushButton, QLabel, QInputDialog, QLineEdit, \
    QGridLayout, QSizePolicy
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 导入自己写的项目模块文件
import GetData
import DataPreprocess
import StockEnvironment
import Runner

global _symbol
global _split_ratio
global _epochs


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 主窗口标题
        self.title = 'DQN Trader'
        # 主窗口宽度
        self.width = 640
        # 主窗口高度
        self.height = 400
        self.thread = MyThread()
        # 初始化UI界面
        self.initUI()

    def initUI(self):

        # 设置主窗口高度和宽度
        self.resize(self.width, self.height)
        # 设置主窗口位置居中
        self.center()
        # self.setGeometry(200, 200, 500, 500)
        # 设置窗口标题
        self.setWindowTitle(self.title)
        # 设置窗口的图标
        self.setWindowIcon(QIcon('icon.png'))

        # 获取输入参数
        # 获取symbol并更新UI
        self.symbol = QLabel('Symbol (example: AAPL)')
        self.symbol_button = QPushButton('Input')
        self.symbol_button.clicked.connect(self.getSymbol)
        # 获取split ratio并更新界面
        self.split_ratio = QLabel('Split Ratio')
        self.split_ratio_button = QPushButton('Input')
        self.split_ratio_button.clicked.connect(self.getSplitRatio)
        # 获取epochs并更新界面
        self.epochs = QLabel('Train Epochs')
        self.epochs_button = QPushButton('Input')
        self.epochs_button.clicked.connect(self.getEpochs)

        # 开始训练
        self.start_button = QPushButton('Start')
        # self.start_button.resize(140,100)
        # 点击按钮后，触发事件，传递参数用于训练
        self.start_button.clicked.connect(self.buttonClicked)

        # 用于显示进度 - 文字提示：Epoch {}: Complete! Final Fortune: {} (Inclue Cash: {})
        self.show_progress = QLabel("Wait to start training...")

        # 用于显示结果 - 图表展示买卖点：red - 买入； green - 卖出； 无标记 - 持有 or 观望
        self.show_result = PlotCanvas(self, width=5, height=4)

        # 盒布局
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        # 添加按钮输入symbol
        self.grid.addWidget(self.symbol, 1, 0)
        self.grid.addWidget(self.symbol_button, 1, 1)
        # 添加按钮输入split ratio
        self.grid.addWidget(self.split_ratio, 2, 0)
        self.grid.addWidget(self.split_ratio_button, 2, 1)
        # 添加按钮输入epochs
        self.grid.addWidget(self.epochs, 3, 0)
        self.grid.addWidget(self.epochs_button, 3, 1)
        # 添加按钮开始训练
        self.grid.addWidget(self.start_button, 4, 0, 1, 2)
        # 添加标签展示训练进度
        self.grid.addWidget(self.show_progress, 5, 0, 1, 2)
        # 添加画布展示图表
        self.grid.addWidget(self.show_result, 6, 0, 5, 2)

        self.setLayout(self.grid)

        # 显示窗口
        self.show()

    # 窗口居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 获取symbol
    def getSymbol(self):
        global _symbol
        s, okPressed = QInputDialog.getText(self, "Symbol", "Name:", QLineEdit.Normal, "")
        if okPressed and s != '':
            text = "Symbol: {0}".format(s)
            self.symbol.setText(text)
            _symbol = s

    # 获取split ratio
    def getSplitRatio(self):
        global _split_ratio
        sp_r, okPressed = QInputDialog.getDouble(self, "Split Ratio", "Value:", 0.7, 0.1, 1.0, 1)
        if okPressed:
            text = "Split Ratio: {0}".format(sp_r)
            self.split_ratio.setText(text)
            _split_ratio = sp_r

    # 获取epochs
    def getEpochs(self):
        global _epochs
        e, okPressed = QInputDialog.getInt(self, "Epochs", "Value:", 5, 1, 100, 1)
        if okPressed:
            text = "Epochs: {0}".format(e)
            self.epochs.setText(text)
            _epochs = e

    # button点击事件,启动子线程执行任务，任务完毕后更新UI
    def buttonClicked(self):
        # 进度提示
        self.show_progress.setText("Start training. Please wait for a moment...")
        # 点击后设置按钮为不可用状态
        self.start_button.setEnabled(False)

        # self.thread = MyThread()
        self.thread.signal.connect(self.callback)
        # 启动线程
        self.thread.start()

    def callback(self, d, a, f, c):
        self.show_progress.setText("Completed! Final Fortune (Total): {} Final Cash (Hold): {}".format(f[-1], c[-1]))
        self.show_result.plot_trade_point(d, a)
        # 退出线程
        self.thread.quit()
        self.thread.wait()
        self.start_button.setEnabled(True)


class MyThread(QThread):
    global _symbol
    global _split_ratio
    global _epochs
    # 定义信号类型，括号里填写信号传递的参数
    signal = pyqtSignal(np.ndarray, list, list, list)

    # 初始化方法
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    # 通过start启动线程后，自动调用run方法中的内容
    def run(self):
        # 进行任务操作
        # 根据用户输入的symbol 从本地读取已下载数据 或 从Quandl获取数据 默认获取最近500条数据
        if _symbol == None:
            print("input _symbol is None!")
            return
        data = GetData.get_data(_symbol)

        # 数据预处理 根据用户输入的split_ratio 返回划分好的训练集和测试集
        train, test = DataPreprocess.data_preprocess(data, _split_ratio)

        # 生成训练环境和测试环境
        env_train = StockEnvironment.StockEnv(train)
        env_test = StockEnvironment.StockEnv(test)

        # 初始化runner
        runner = Runner.Runner()
        # 训练dqn网络，返回训练完毕的模型，以及训练最终结果; 显示训练情况图
        trained_model = runner.trainer(_symbol, env_train, _epochs)

        for new_dir in os.listdir(os.curdir):  # 列表出该目录下的所有文件(返回当前目录'.')
            # 如果有success的模型就使用，否则使用train模型
            if new_dir.startswith('success-model-{}'.format(_symbol)):
                trained_model = new_dir

        print('Model Name: {}'.format(trained_model))

        # 用训练后的trained_Q对test数据进行分析，给出预测出的最终交易行为；显示测试情况图
        fortune, act, reward, cash = runner.tester(env_test, trained_model)
        d = test
        a = act
        f = fortune
        c = cash
        # 预测说明：
        #          模型仅预测当天的交易行为，输入模型的数据为历史数据，
        #		   历史数据指的不是train数据集，而是test数据集的数据
        # PlotTradePoint.plot_trade_point(test, act, x_name='Test - Steps', y_name='Test - Close Price')

        # 任务完成，发射信号
        self.signal.emit(d, a, f, c)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # 载入 X 轴名称
        self.x_name = "Steps"
        # 设置 Y 轴名称
        self.y_name = "Close Price"

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot_default_fig()

    def plot_default_fig(self):
        # 随机数 - 用于测试
        data = [np.random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(np.arange(len(data)), data)
        ax.set_xlim((0, len(data)))
        ax.set_ylim((np.min(data), np.max(data)))
        ax.set_xlabel(self.x_name)
        ax.set_ylabel(self.y_name)
        ax.set_title('DQN Trader Random Example')
        self.draw()

    def plot_trade_point(self, data, act_list):
        # 载入数据 data，从中获取 Close Price
        self.close_price = data[5:, 3]
        # 载入数据 act_list，从中获取 Act
        self.act = act_list
        # 新增画布
        ax = self.figure.add_subplot(111)
        # 画布上添加 Close Price
        ax.plot(np.arange(len(self.close_price)), self.close_price)
        # 调整 X 轴坐标
        ax.set_xlim((0, len(self.close_price)))
        # 调整 Y 轴坐标
        ax.set_ylim((np.min(self.close_price), np.max(self.close_price)))
        # 设置 X 轴名称
        ax.set_xlabel(self.x_name)
        # 设置 Y 轴名称
        ax.set_ylabel(self.y_name)
        # 设置图标名称
        ax.set_title('Trade Point predicted by DQN Trader')

        for i in range(len(self.act)):
            if self.act[i] == 1:
                ax.scatter(x=i, y=self.close_price[i], c='r', marker='o', linewidths=0, label='Buy')
            if self.act[i] == 2:
                ax.scatter(x=i, y=self.close_price[i], c='g', marker='o', linewidths=0, label='Sell')

        # 显示图标
        self.draw()


def test_model(symbol="AAPL", split_ratio=0.8, epochs=1, n_samples=500, isTrain=False):
    _symbol = symbol
    _split_ratio = split_ratio
    _epochs = epochs
    data = GetData.get_A_data(ts_code=_symbol, n_samples=n_samples)
    print(data.columns.values)
    # 数据预处理 根据用户输入的split_ratio 返回划分好的训练集和测试集
    # train, test, date_train, date_test = DataPreprocess.data_preprocess(data, _split_ratio)
    train, test, date_train, date_test = DataPreprocess.data_A_preprocess(data, _split_ratio)

    # 生成训练环境和测试环境
    env_test = StockEnvironment.StockEnv(test)
    env_train = StockEnvironment.StockEnv(train)

    # 初始化runner
    runner = Runner.Runner()
    trained_model = None
    if isTrain == False:
        for new_dir in os.listdir(os.curdir):  # 列表出该目录下的所有文件(返回当前目录'.')
            # 如果有success的模型就使用，否则使用train模型
            if new_dir.startswith('success-model-{}'.format(_symbol)):
                trained_model = new_dir
        # 如果没有success模型，使用训练过的train模型
        if trained_model == None:
            for dir_name in os.listdir(os.curdir):  # 列表出该目录下的所有文件(返回当前目录'.')
                if dir_name.startswith('train-model-{}'.format(_symbol)):
                    trained_model = dir_name
        if trained_model == None:
            print("No model for predict,now train a model")
            trained_model = runner.trainer(_symbol, env_train, _epochs)
    else:
        # 训练dqn网络，返回训练完毕的模型，以及训练最终结果; 显示训练情况图
        trained_model = runner.trainer(_symbol, env_train, _epochs)
    print('Model Name: {}'.format(trained_model))
    # 用训练后的trained_Q对test数据进行分析，给出预测出的最终交易行为；显示测试情况图
    fortune, act, reward, cash = runner.tester(env_test, trained_model)
    print("profitRatio:{},fortune:{},act:{},reward:{},cash:{}".format(fortune[-1] / 100000.0, fortune[-1], act[-1],
                                                                      reward[-1], cash[-1]))
    print("fortune len:", len(fortune))
    return test, act, fortune, cash, date_test


def compute_profit_ratio(data):
    if data.__len__() == 0:
        print("data size is 0")
        return
    base = data[0]
    result = []
    for d in data:
        result.append((d / base - 1.0) * 100)
    return result


def plt_data(test, act, fortune, cash, date_test, symbol):
    d = test
    a = act
    f = fortune
    c = cash
    dt = date_test
    close_price = d[5:, 3]
    # --获取date数据
    # 载入数据 act_list，从中获取 Act
    act = a
    # 新增画布
    fig = plt.figure()

    # 绘制股价交易图
    ax = fig.add_subplot(211)
    # 画布上添加 Close Price
    ax.plot(np.arange(len(close_price)), close_price)
    print(dt.shape)
    date_list = []
    for d in dt[5:]:
        date_list.append(d)
    ax_xticks_label = []
    ax.set_xticks(np.arange(0, len(date_list), 10))
    x_tick_labels = []
    i = 0
    for item in date_list:
        if (i % 10) == 0:
            ax_xticks_label.append(item)
        i += 1
    ax.set_xticklabels(ax_xticks_label)

    # 调整 X 轴坐标
    ax.set_xlim((0, len(close_price)))
    # 调整 Y 轴坐标
    ax.set_ylim((np.min(close_price), np.max(close_price)))
    # 设置 X 轴名称
    ax.set_xlabel("Date")
    # 设置 Y 轴名称
    ax.set_ylabel("Stock Price")
    # 设置图标名称
    ax.set_title('Trade Point predicted for {}'.format(symbol))
    for i in range(len(act)):
        if act[i] == 1:
            type1 = ax.scatter(x=i, y=close_price[i], c='r', marker='o', linewidths=0, label='Buy')
        if act[i] == 2:
            type2 = ax.scatter(x=i, y=close_price[i], c='g', marker='o', linewidths=0, label='Sell')
            # 显示图标

    # 绘制收益率折线图
    ax1 = fig.add_subplot(212)
    plot_fortune = [(i / 100000 - 1.0) * 100 for i in fortune]
    print("plot_fortuen.len:", plot_fortune.__len__())
    f_type1 = ax1.plot(np.arange(len(fortune)), plot_fortune, color='red', linewidth=1.0, label=symbol)
    date_list1 = []
    for d in dt[5:]:
        date_list1.append(d)
    ax1.set_xticks(np.arange(0, len(date_list1), 10))
    x_tick_labels = []
    i = 0
    for item in date_list1:
        if (i % 10) == 0:
            x_tick_labels.append(item)
        i += 1

    ax1.set_xticklabels(x_tick_labels)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Fortune(%)")
    ax1.set_title("Fortune Figure for {}".format(symbol))

    # 将基准沪深300收益率作为比较基准
    print("date_list:", date_list1[0], date_list1[-1])
    hs300_data = GetData.get_stock(ts_code="399300.SZ", start_date=date_list1[0], end_date=date_list1[-1])
    print("hs300_data.shape:", hs300_data.shape)
    hs300_profit_ratio = compute_profit_ratio(hs300_data['close'].values)

    print("hs300 length:", (hs300_profit_ratio.__len__()))
    print("hs300_profit_ratio.len:", hs300_profit_ratio.__len__())
    f_type2 = ax1.plot(np.arange(len(date_list1)), hs300_profit_ratio, color='black', linewidth=1.0,
                       linestyle='--', label="hs300")

    # ax1.legend(handles=[f_type1, f_type2], labels=['a', 'b', ], loc='best',fontsize="small")
    # 收益率为0的基准线

    plt.show()


def getPlotData(test, act, fortune, cash, date_test, symbol):
    d = test
    a = act
    f = fortune
    c = cash
    dt = date_test
    close_price = d[5:, 3]
    # --获取date数据
    # 载入数据 act_list，从中获取 Act
    act = a
    # 新增画布
    fig = plt.figure()

    # 绘制股价交易图
    ax = fig.add_subplot(211)
    # 画布上添加 Close Price
    ax.plot(np.arange(len(close_price)), close_price)
    print(dt.shape)
    date_list = []
    for d in dt[5:]:
        date_list.append(d)
    ax_xticks_label = []
    ax.set_xticks(np.arange(0, len(date_list), 10))
    x_tick_labels = []
    i = 0
    for item in date_list:
        if (i % 10) == 0:
            ax_xticks_label.append(item)
        i += 1
    ax.set_xticklabels(ax_xticks_label)

    # 调整 X 轴坐标
    ax.set_xlim((0, len(close_price)))
    # 调整 Y 轴坐标
    ax.set_ylim((np.min(close_price), np.max(close_price)))
    # 设置 X 轴名称
    ax.set_xlabel("Date")
    # 设置 Y 轴名称
    ax.set_ylabel("Stock Price")
    # 设置图标名称
    ax.set_title('Trade Point predicted for {}'.format(symbol))
    for i in range(len(act)):
        if act[i] == 1:
            type1 = ax.scatter(x=i, y=close_price[i], c='r', marker='o', linewidths=0, label='Buy')
        if act[i] == 2:
            type2 = ax.scatter(x=i, y=close_price[i], c='g', marker='o', linewidths=0, label='Sell')
            # 显示图标

    # 绘制收益率折线图
    ax1 = fig.add_subplot(212)
    plot_fortune = [(i / 100000 - 1.0) * 100 for i in fortune]
    print("plot_fortuen.len:", plot_fortune.__len__())
    f_type1 = ax1.plot(np.arange(len(fortune)), plot_fortune, color='red', linewidth=1.0, label=symbol)
    date_list1 = []
    for d in dt[5:]:
        date_list1.append(d)
    ax1.set_xticks(np.arange(0, len(date_list1), 10))
    x_tick_labels = []
    i = 0
    for item in date_list1:
        if (i % 10) == 0:
            x_tick_labels.append(item)
        i += 1

    ax1.set_xticklabels(x_tick_labels)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Fortune(%)")
    ax1.set_title("Fortune Figure for {}".format(symbol))

    # 将基准沪深300收益率作为比较基准
    print("date_list:", date_list1[0], date_list1[-1])
    hs300_data = GetData.get_stock(ts_code="399300.SZ", start_date=date_list1[0], end_date=date_list1[-1])
    print("hs300_data.shape:", hs300_data.shape)
    hs300_profit_ratio = compute_profit_ratio(hs300_data['close'].values)

    print("hs300 length:", (hs300_profit_ratio.__len__()))
    print("hs300_profit_ratio.len:", hs300_profit_ratio.__len__())
    f_type2 = ax1.plot(np.arange(len(date_list1)), hs300_profit_ratio, color='black', linewidth=1.0,
                       linestyle='--', label="hs300")

    # ax1.legend(handles=[f_type1, f_type2], labels=['a', 'b', ], loc='best',fontsize="small")
    # 收益率为0的基准线

    # plt.show()


    # ---------
    df_result = pd.DataFrame([])
    df_result['date'] = date_list
    df_result['action'] = act
    df_result['target_price'] = close_price
    df_result['hs300_profit_ratio'] = hs300_profit_ratio
    df_result['profit_ratio'] = plot_fortune
    return df_result


def init():
    # 获取对应公司的数据
    symbol = "600519.SH"
    split_ratio = 0.8
    epochs = 1
    n_samples = 1000
    isTrain = False
    # 获取模型在股价上的数据
    test, act, fortune, cash, date_test = test_model(symbol, split_ratio, epochs, n_samples, isTrain)
    # 将数据在图像上画出
    plt_data(test, act, fortune, cash, date_test, symbol)

def getBackTestData(symbol='600519.SH',epochs=1,n_samples=1000,isTrain=False):
    # 获取对应公司的数据
    split_ratio = 0.8
    epochs = 1
    # 获取模型在股价上的数据
    test, act, fortune, cash, date_test = test_model(symbol, split_ratio, epochs, n_samples, isTrain)
    # 将数据在图像上画出
    result=getPlotData(test, act, fortune, cash, date_test, symbol)
    return result


if __name__ == '__main__':
    # 启动界面程序
    # app = QApplication(sys.argv)
    # mw = MainWindow()
    # sys.exit(app.exec_())

    # 训练绘图
    init()
