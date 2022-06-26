#-*- coding: utf-8 -*-
"""
This module contains some tools to handle the indicators of strategy.
"""


def CrossOver(data1, data2):
    """
    输入Get_Data类的数据
    
    data1向上穿过data2返回 1, data1向下穿过data2返回 -1, 不发生交叉则返回 0
    """
    if data1(-1) < data2(-1) and data1(0) > data2(0): return 1
    if data1(-1) > data2(-1) and data1(0) < data2(0): return -1
    else: return 0

def income(buy_price, sell_price, size, commission):
    """
    计算收益
    """
    return (sell_price - buy_price) * size - commission