#-*- coding: utf-8 -*-
"""
该模块用于操作交易, 包括模拟交易和实盘交易
"""
import datetime

from ding import Messenger
import utils


class Order():
    """
    命令基类, 基本买入卖出平仓命令
    """
    def __init__(self, broker: dict):
        self.cash = broker['cash']  # 资金
        self.commission = broker['commission']  # 手续费
        self.value = self.cash
        self.buy_price = None  # 买入价格
        self.sell_price = None  # 卖出价格
        self.size = None  # 买入数量

    def buy(self):
        pass

    def sell(self):
        pass

    def close(self):
        pass

    def get_now(self):
        """
        获取当前时间
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Real(Order, Messenger):
    """
    实盘交易类
    """
    def __init__(self, dingtokens: dict):
        Messenger.__init__(self,
                           token=dingtokens['token'],
                           secret=dingtokens['secret'])

    def buy(self, exchange, symbol, price, size):
        # 操作


        # 发送消息
        title = "{}买入成功".format(symbol)
        text = "##  实盘交易信息\n\n**交易所:** {}\n\n**买入交易对:** {}\n\n**买入时间:** {}\n\n**买入价格:** {}".format(
            exchange, symbol, self.get_now(), str(price))
        data = {"title": title, "text": text}
        self.sendMarkdown(data)

    def sell(self, exchange, symbol, price, size):
        ...

    def close(self, exchange, symbol, price, size):
        ...


class Simu(Order, Messenger):
    """
    模拟交易类
    """
    def __init__(self,
                 broker: dict = {
                     'cash': 10000,
                     'commission': 0
                 },
                 dingtokens: dict = {
                     'token': None,
                     'secret': None
                 }):
        Order.__init__(self, broker)
        Messenger.__init__(self,
                           token=dingtokens['token'],
                           secret=dingtokens['secret'])

    def buy(self, exchange, symbol: str, price: float, size=None):
        """买入"""
        self.buy_price = price
        self.size = size

        # 发送消息
        title = "{}买入成功".format(symbol)
        text = "##  交易信息\n\n**交易所:** {}\n\n**买入交易对:** {}\n\n**买入时间:** {}\n\n**买入价格:** {}".format(
            exchange, symbol, self.get_now(), str(price))
        data = {"title": title, "text": text}
        self.sendMarkdown(data)

    def sell(self, exchange, symbol, price, size):
        self.sell_price = price
        income = utils.income(self.buy_price, self.sell_price, size,
                              self.commission)
        self.cash += income

        # 发送消息
        title = "{}卖出成功".format(symbol)
        text = "##  交易信息\n\n**交易所:** {}\n\n**卖出交易对:** {}\n\n**时间:** {}\n\n**卖出价格:** {}".format(
            exchange, symbol, self.get_now(), str(price))
        data = {"title": title, "text": text}
        self.sendMarkdown(data)

    def close(self, exchange, symbol, price, size):
        self.close_price = price
        income = utils.income(self.buy_price, self.sell_price, size,
                              self.commission)
        self.cash += income
        # 发送消息
        title = "{}卖出成功".format(symbol)
        text = "##  交易信息\n\n**交易所:** {}\n\n**卖出交易对:** {}\n\n**时间:** {}\n\n**卖出价格:** {}".format(
            exchange, symbol, self.get_now(), str(price))
        data = {"title": title, "text": text}
        self.sendMarkdown(data)


class Operator():
    """
    Real类和Simu类的多态实现

    @param order: Real类或Simu类的实例
    """
    def __init__(
        self,
        order,
    ):
        self.order = order  # Simu 类或 Real 类

    def buy(self, exchange, symbol: str, price: float, size=None):
        self.order.buy(exchange, symbol, price, size)

    def sell(self, exchange, symbol: str, price: float, size=None):
        self.order.sell(exchange, symbol, price, size)

    def close(self, exchange, symbol: str, price: float, size=None):
        self.order.close(exchange, symbol, price, size)


if __name__ == "__main__":
    dingtokens = {
        'token':
        'b9f1d4824cb3cb8b619f2eafc511a7c017ee5746137a2f0c303354174622a76d',
        'secret':
        'SECfb56c244c3b7b2aa23548a307e7397d1427be12843ed175b1632d712b8c8f010'
    }
    simu = Simu(dingtokens=dingtokens)
    real = Real(dingtokens=dingtokens)
    operator = Operator(simu)
    operator.buy('binance', 'ETHUSDT', 1000.0)
    operator.sell('binance', 'ETHUSDT', 1200.0)
    operator.close('binance', 'ETHUSDT', 1200.0)