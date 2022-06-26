import backtrader as bt


class SMA(bt.Strategy):
    """
    SMA(Simple Moving Average)
    计算公式: MA = (C1 + C2 + C3 + ... + Cn) / n, Cn是时刻 n 的收盘价。
    """
    params = (('period', 10),)

    def __init__(self):
        self.sma = bt.indicators.MovingAverageSimple(self.data, self.p.period)
        self.buy_signal = bt.indicators.CrossOver(self.data.close, self.sma)

    def next(self):
        if not self.position and self.buy_signal[0] == 1:
            self.order = self.buy()
        if not self.position and self.buy_signal[0] == -1:
            self.order = self.sell()
        if self.position and self.buy_signal[0] == 1:
            self.order = self.close()  # 清仓
            self.order = self.buy()
        if self.position and self.buy_signal[0] == -1:
            self.order = self.close()  # 清仓
            self.order = self.sell()