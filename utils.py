import ccxt
import pandas as pd
import os


def getHistoryData(exchange, symbol: str, timeframe: str, since=None):
    '''
    获取交易对的历史数据，
    '''
    if not os.path.exists('history_data/'): os.mkdir('history_data/')
    kldata = exchange.fetch_ohlcv(symbol, timeframe, since)
    # reverse timestamp to specific format
    # for row in kldata:
    #     _ = time.localtime(row[0] / 1000)
    #     row[0] = time.strftime("%Y-%m-%d %H:%M:%S", _)
    df_kl = pd.DataFrame(
        kldata, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    # save csv file
    filename = symbol.replace('/', '') + '_' + str(timeframe.upper()) + '.csv'
    df_kl.to_csv('history_data/' + filename, index=0)


# test
if __name__ == '__main__':
    binance = ccxt.binance(
        {'proxies': {
            'http': '127.0.0.1:7890',
            'https': '127.0.0.1:7890'
        }})
    getHistoryData(binance, 'BTC/USDT', '1d')
    getHistoryData(binance, 'ETH/USDT', '1d')
    getHistoryData(binance, 'BTC/USDT', '1h')
    getHistoryData(binance, 'ETH/USDT', '1h')