#-*- coding: utf-8 -*-
"""
This module is used to process datas.

"""
import os

import pandas as pd


def getHistoryData(exchange, symbol: str, timeframe: str, since=None):
    '''
    获取交易对的历史数据

    Args:
    ---
    exchange: ccxt所支持的交易所
    symbol: 交易对
    timeframe: 历史数据的获取频率
    since: 开始日期
    '''

    if not os.path.exists('../history_data/'): os.mkdir('../history_data/')
    kldata = exchange.fetch_ohlcv(symbol, timeframe, since)
    # reverse timestamp to specific format
    # for row in kldata:
    #     _ = time.localtime(row[0] / 1000)
    #     row[0] = time.strftime("%Y-%m-%d %H:%M:%S", _)
    df_kl = pd.DataFrame(
        kldata, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    # save csv file
    filename = symbol.replace('/', '') + '_' + str(timeframe.upper()) + '.csv'
    df_kl.to_csv('../history_data/' + filename, index=0)


class LineData():
    """
    获取CSV历史数据, 包括datetime, open, high, low, close, volume

    @param int index: 0 代表当前数据(今天), -1 代表上一个数据(昨天)

    该类还需进一步开发
    """
    def __init__(self, csvfile: str):
        dataframe = pd.read_csv(csvfile)
        dataframe['datetime'] = pd.to_datetime(dataframe['datetime'],
                                               unit="ms")
        self.data = dataframe
        self.index = 0
        self.date_line = dataframe['datetime'].values
        self.open_line = dataframe['open'].values
        self.high_line = dataframe['high'].values
        self.low_line = dataframe['low'].values
        self.close_line = dataframe['close'].values
        self.volume_line = dataframe['volume'].values

    def pindex(self):
        print('Index shouldn\'t a positive number.')

    def date(self, index=0):
        self.index = index
        if self.index - 1 > 0:
            self.pindex()
            return
        return self.date_line[self.index - 1]

    def open(self, index=0):
        self.index = index
        if self.index - 1 > 0:
            self.pindex()
            return
        return self.open_line[self.index - 1]

    def high(self, index=0):
        self.index = index
        if self.index - 1 > 0:
            self.pindex()
            return
        return self.high_line[self.index - 1]

    def low(self, index=0):
        self.index = index
        if self.index - 1 > 0:
            self.pindex()
            return
        return self.low_line[self.index - 1]

    def close(self, index=0):
        self.index = index
        if self.index - 1 > 0:
            self.pindex()
            return
        return self.close_line[self.index - 1]

    def volume(self, index=0):
        self.index = index
        if self.index - 1 > 0:
            self.pindex()
            return
        return self.volume_line[self.index - 1]


# test
if __name__ == '__main__':
    import ccxt
    binance = ccxt.binance(
        {'proxies': {
            'http': '127.0.0.1:7890',
            'https': '127.0.0.1:7890'
        }})
    print(type(binance))
    # getHistoryData(binance, 'ETHUSDT', '1d')
    # getHistoryData(binance, 'ETHUSDT', '1h')
    # getHistoryData(binance, 'BTCUSDT', '1d')
    # getHistoryData(binance, 'BTCUSDT', '1h')