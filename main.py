import backtrader as bt
import datetime
import pandas as pd
import csv
from strategy.test import TestStrategy

if __name__ == '__main__':

    # 初始化模型
    cerebro = bt.Cerebro()

    # 构建策略
    strats = cerebro.addstrategy(TestStrategy)

    # 每次买100股
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # 加载数据到模型中
    dataname = 'history_data/BTCUSDT_1D.csv'
    # Pandas
    dataframe = pd.read_csv(dataname)
    dataframe['datetime'] = pd.to_datetime(dataframe['datetime'], format="%Y-%m-%dT%H:%M:%S")
    dataframe.set_index('datetime', inplace=True)
    data = bt.feeds.PandasData(dataname=dataframe,)
                            #    fromdate=datetime.datetime(2022, 1, 1),
                            #    todate=datetime.datetime(2022, 6, 1))
    # CSV
    # dataframe = pd.read_csv("history_data/BTCUSDT_1D.csv")
    # dataframe['datetime'] = pd.to_datetime(dataframe['datetime'], format="%Y-%m-%d %H:%M:%S")
    # data = bt.feeds.GenericCSVData(dataname=dataname,
    #                                fromdate=datetime.datetime(2021, 2, 2),
    #                                todate=datetime.datetime(2022, 6, 16),
    #                                dtformat=('%Y-%m-%d %H:%M:%S'))

    # 导入数据
    cerebro.adddata(data)

    # 设定初始资金和佣金
    cerebro.broker.setcash(1000000.0)
    cerebro.broker.setcommission(0.005)

    # 策略执行前的资金
    # print('启动资金: %.2f' % cerebro.broker.getvalue())

    # 策略执行
    cerebro.run()

    # 绘图
    cerebro.plot()
