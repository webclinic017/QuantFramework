#-*- coding: utf-8 -*-
"""
This module is used to cend massage to DingTalk.

Author: Foryoung Yu
Email: foryoung_yu@outlook.com
"""

import base64
import datetime
import hashlib
import hmac
import json
import os
import time
from urllib.parse import quote_plus

import requests


def getNewPrice(exchange, symbol: str):
    """
    获取某个交易所的某个货币价格, 常与Message.send_markdown连用
    return: markdown格式报价
    """
    if (exchange.has['fetchTickers']):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ticker = exchange.fetch_ticker(symbol)
        open = ticker['open']
        high = ticker['high']
        low = ticker['low']
        close = ticker['close']
        lastPrice = ticker['last']
        vwap = ticker['vwap']
        percentage = ticker['percentage']

        title = "{}报价".format(symbol)
        text = "### {}最新报价\n\n**上海时间：** {}\n\n**最新价格：** {}\n\n**涨跌幅：** {}%\n\n".format(
            symbol, now, lastPrice, percentage)
        data = {"title": title, "text": text}
        return data
    else:
        title = "价格获取失败"
        text = "小秘书提醒您：该交易所不支持获取行情"
        data = {"title": title, "text": text}
        return data


class Messenger():
    """
    向钉钉发送消息
    """
    def __init__(self,
                 token=os.getenv("DD_ACCESS_TOKEN"),
                 secret=os.getenv("DD_SECRET")):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc,
                             string_to_sign_enc,
                             digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}

    def sendText(self, content):
        """
        发送单个文本消息
        @param content: str, 文本内容
        """
        data = {"msgtype": "text", "text": {"content": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(url=self.URL,
                             data=json.dumps(data),
                             params=self.params,
                             headers=self.headers)

    def sendMarkdown(self, content):
        """
        发送 MarkDown 消息
        """
        data = {"msgtype": "markdown", "markdown": content}
        self.params["timestamp"] = self.timestamp
        return requests.post(url=self.URL,
                             data=json.dumps(data),
                             params=self.params,
                             headers=self.headers)

    def sendNewPrice(self, exchange, symbol):
        """
        发送最新价格的 MarkDown 消息

        Args: 
        ---
        - exchange: str
            交易所
        - symbol: str
            交易对
        """
        content = getNewPrice(exchange, symbol)
        data = {"msgtype": "markdown", "markdown": content}
        self.params["timestamp"] = self.timestamp
        return requests.post(url=self.URL,
                             data=json.dumps(data),
                             params=self.params,
                             headers=self.headers)


# test
if __name__ == "__main__":
    import ccxt
    bot = Messenger(
        token=
        'b9f1d4824cb3cb8b619f2eafc511a7c017ee5746137a2f0c303354174622a76d',
        secret=
        'SECfb56c244c3b7b2aa23548a307e7397d1427be12843ed175b1632d712b8c8f010')
    binance = ccxt.binance(
        {'proxies': {
            'http': '127.0.0.1:7890',
            'https': '127.0.0.1:7890'
        }})
    bot.sendNewPrice(binance, 'ETHUSDT')