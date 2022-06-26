import backtrader as bt


class DEMA(bt.Strategy):
    def __init__(self):
        self.dema = bt.indicators.DEMA(self.data)  # DEMA
        self.buy_sig = bt.indicators.CrossOver(self.data.close[0], self.dema[0])
        # self.sell_sig = bt.indicators.CrossDown(self.data.close[0], self.dema[0])

    def next(self):
        if self.order: return # 判断是否有交易正在进行
        if not self.position and self.buy_sig[0] == 1:
            self.order = self.buy()
        if not self.position and self.buy_sig[0] == -1:
            return
            # self.order = self.sell()
        if self.getposition().size < 0 and self.buy_sig[0] == 1:
            self.order = self.close()
            self.order = self.buy()
        if self.getposition().size > 0 and self.buy_sig[0] == -1:
            self.order = self.close()
            self.order = self.sell()