import csv
import datetime

import backtrader as bt
import pandas as pd

# import strategy.SMA
from strategy.DEMA import DEMA
from strategy.Three_bars import MyStrategy

if __name__ == '__main__':

    # 初始化模型
    cerebro = bt.Cerebro()

    # 构建策略
    mystrategy = DEMA
    strats = cerebro.addstrategy(strategy=mystrategy)

    # 加载数据到模型中
    dataname = 'history_data/ETHUSDT_1D.csv'
    dataframe = pd.read_csv(dataname)
    dataframe['datetime'] = pd.to_datetime(dataframe['datetime'],
                                           unit="ms")  # 转换日期格式

    # print(dataframe)

    dataframe.set_index('datetime', inplace=True)
    data = bt.feeds.PandasData(dataname=dataframe,
                               fromdate=datetime.datetime(2022, 1, 1),
                               todate=datetime.datetime(2022, 6, 21))

    #    timeframe=bt.TimeFrame.Minutes)

    # 导入数据
    cerebro.adddata(data)
    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Days)

    # 设定初始资金和佣金
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(0.005)
    # cerebro.broker.set_filler(bt.broker.filler.FixedBarPerc(perc=0.1))
    # cerebro.broker.set_filler(bt.broker.filler.FixedSize(size=1))

    # 策略执行前的资金
    print('启动资金: %.2f' % cerebro.broker.getvalue())
    print(cerebro.broker.getcash())

    # 策略执行
    cerebro.run()
    print('执行策略后的资金: %.2f' % cerebro.broker.getvalue())

    # 绘图
    cerebro.plot(style="candle")
