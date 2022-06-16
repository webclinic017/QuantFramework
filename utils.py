import ccxt
import pandas as pd
import os


def getHistoryData(exchange, symbol: str, timeframe: str):
    '''获取交易对的历史数据，
    '''
    if not os.path.exists('history_data/'): os.mkdir('history_data/')
    kldata = exchange.fetch_ohlcv(symbol, timeframe)
    df_kl = pd.DataFrame(
        kldata, columns=['DataTime', 'Open', 'High', 'Low', 'Close', 'Volume'])

    filename = symbol.replace('/', '_') + '_' + str(timeframe.upper()) + '.csv'
    df_kl.to_csv('historyData/' + filename, index=0)


# test
if __name__ == '__main__':
    binance = ccxt.binance(
        {'proxies': {
            'http': '127.0.0.1:7890',
            'https': '127.0.0.1:7890'
        }})
    getHistoryData(binance, 'ETH/USDT', '1d')
    getHistoryData(binance, 'BTC/USDT', '1d')