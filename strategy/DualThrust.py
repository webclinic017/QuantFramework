import backtrader as bt


class DT_Line(bt.Indicator):
    lines = ('U', 'D')
    params = (('period', 2), ('k_u', 0.7), ('k_d', 0.7))

    def __init__(self):
        self.addminperiod(self.p.period + 1)  # p = params

    def next(self):
        HH = max(self.data.high.get(-1, size=self.p.period))  # n日High的最高价
        LC = min(self.data.close.get(-1, size=self.p.period))  # n日close的最低价
        HC = max(self.data.close.get(-1, size=self.p.period))  # n日close的最高价
        LL = min(self.data.low.get(-1, size=self.p.period))  # n日low的最低价
        R = max(HH - LC, HC - LL)
        self.lines.U[0] = self.data.open[0] + self.p.k_u * R
        self.lines.D[0] = self.data.open[0] - self.p.k_d * R


class DualThrust(bt.Strategy):
    def __init__(self):
        self.dataclose = self.data0.close
        self.D_Line = DT_Line(self.data1)
        self.D_Line = self.D_Line()
        # self.D_Line.plotinfo.plot = False
        self.D_Line.plotinfo.plotmaster = self.data0

        self.buy_signal = bt.indicators.CrossOver(self.dataclose,
                                                  self.D_Line.U)
        self.sell_signal = bt.indicators.CrossDown(self.dataclose,
                                                   self.D_Line.D)

    def next(self):
        if not self.position and self.buy_signal[0] == 1:
            self.order = self.buy()
        if not self.position and self.sell_signal[0] == 1:
            self.order = self.sell()
        if self.getposition().size < 0 and self.buy_signal[0] == 1:
            self.order = self.close()
            self.order = self.buy()
        if self.getposition().size > 0 and self.sell_signal[0] == 1:
            self.order = self.close()
            self.order = self.sell()

    # def stop(self):
    #     print("period: %s, k_u: %s, k_d: %s, final_value: %.2f" %
    #           (self.p.period, self.p.k_u, self.broker.getvalue()))
