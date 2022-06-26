import backtrader as bt


class three_bars(bt.Indicator):
    lines = ('up', 'down')

    def __init__(self):
        self.addminperiod(4)  # 最小开始周期
        # self.plotinfo.plotmaster = self.data
        self.plotinfo.plot = False  # 不绘制曲线

    def next(self):
        self.up[0] = max(max(self.data.close.get(ago=-1, size=3)),
                         max(self.data.open.get(ago=-1, size=3)))
        self.down[0] = min(min(self.data.close.get(ago=-1, size=3)),
                           min(self.data.open.get(ago=-1, size=3)))


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.up_down = three_bars(self.data)
        self.buy_signal = bt.indicators.CrossOver(self.data.close,
                                                  self.up_down.up)
        self.sell_signal = bt.indicators.CrossDown(self.data.close,
                                                   self.up_down.down)
        self.buy_signal.plotinfo.plot = False
        self.sell_signal.plotinfo.plot = False

    def next(self):
        if not self.position and self.buy_signal[0] == 1:
            self.order = self.buy()
        if self.getposition().size < 0 and self.buy_signal[0] == 1:
            self.order = self.close()
            self.order = self.buy()
        if not self.position and self.sell_signal[0] == 1:
            self.order = self.sell()
        if self.getposition().size > 0 and self.buy_signal[0] == 1:
            self.order = self.close()
            self.order = self.sell()