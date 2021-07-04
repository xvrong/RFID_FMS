﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2021/06/28
@Author  : LinXuan
@File    : DisplayData
@Function: 展示原始数据
'''
import matplotlib.colors as mcolors
import numpy as np
import math
import matplotlib.pyplot as plt

from pysrc.ObtainData import ObtainData


list_epc = []            # EPC列表
list_time = []           # Time列表
list_phase = []          # PHASE列表
list_rssi = []           # RSSI列表

params = []


def DisplayData(*params, filename="data.txt"):
    '''
        *params :   展示的标签的列表
    '''
    list_epc, list_time, list_phase, list_rssi = ObtainData(
        *params, filename=filename)
    colors = list(mcolors.TABLEAU_COLORS.keys())  # 颜色变化
    len_colors = len(mcolors.TABLEAU_COLORS)  # 颜色长度
    for i in range(0, len(list_epc)):
        plt.scatter(list_time[i], list_phase[i],
                    color=mcolors.TABLEAU_COLORS[colors[i % len_colors]], marker='*')
    plt.legend([str(list_epc[i][0:9]) for i in range(len(list_epc))],
               loc='upper right', fontsize='small')

    plt.show()


def main():
    DisplayData("1e-2c", filename="data\\2021-07-02\\11-29-08.txt")


if __name__ == "__main__":
    main()
