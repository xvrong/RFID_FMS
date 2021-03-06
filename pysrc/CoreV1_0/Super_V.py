#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2021/05/18
@Author  : LinXuan
@File    : Super_V.py
@Function: Super_V拟合，排序
'''
import matplotlib.colors as mcolors
import numpy as np
import math
import matplotlib.pyplot as plt
listen_epc = [
    "FFFF 0011 0000 0000 0000 0000",
    "FFFF 0012 0000 0000 0000 0000",
    "FFFF 0013 0000 0000 0000 0000",
    "FFFF 0014 0000 0000 0000 0000",
    "FFFF 0015 0000 0000 0000 0000",
    "FFFF 0016 0000 0000 0000 0000",
    "FFFF 0017 0000 0000 0000 0000",
    "FFFF 0018 0000 0000 0000 0000",
    "FFFF 0019 0000 0000 0000 0000",
    "FFFF 0020 0000 0000 0000 0000",
    "FFFF 0021 0000 0000 0000 0000",
    "FFFF 0022 0000 0000 0000 0000",
    "FFFF 0023 0000 0000 0000 0000",
    "FFFF 0024 0000 0000 0000 0000",
    "FFFF 0025 0000 0000 0000 0000",
    "FFFF 0026 0000 0000 0000 0000",
    "FFFF 0027 0000 0000 0000 0000",
    "FFFF 0028 0000 0000 0000 0000",
    "FFFF 0029 0000 0000 0000 0000",
]  # 实验中监控的标签列表
list_epc = []            # EPC列表
list_time = []           # Time列表
list_rssi = []           # RSSI列表
list_phase = []          # PHASE列表
first_time = 0           # 初始化一个开始时间，每次获得的开始时间不同


def process(olddata):
    "粘合数据范围"
    size = len(olddata)  # 数据量的大小
    newdata = [0] * size
    ct = 0
    jump = 4
    for i in range(1, size):
        if(olddata[i] - olddata[i - 1] < -jump):
            ct += 1
        elif(olddata[i] - olddata[i - 1] > jump):
            ct -= 1
        newdata[i] = olddata[i] + ct * math.pi * 2
    return newdata


def regression(time, phase):
    "多项式回归， 返回拟合后的数据"
    parameter = np.polyfit(time, phase, 2)
    func = np.poly1d(parameter)
    phase_fit = func(time)
    return phase_fit, -parameter[1] / (2 * parameter[0])


with open("./data.txt") as lines:
    """
    数据处理部分
    分割后的数据： Epc-Time-Rssi-Phase
    """

    for line in lines:
        tag_info = line.split('#')
        if len(tag_info) != 5:                   # 接收的TagInfo长度为4，分别为EPC, Time, Rssi, Phase，错误则开启下一个循环
            continue
        elif tag_info[0] not in listen_epc:
            continue
        else:
            if first_time == 0:                   # 第一次接收到Tag信息，将FirstTime初始化
                first_time = int(tag_info[1])
            if tag_info[0] not in list_epc:       # 若出现新标签，将新标签加入列表，为新标签创建各信息列表
                list_epc.append(tag_info[0])
                list_time.append([])
                list_rssi.append([])
                list_phase.append([])
            tag_index = list_epc.index(tag_info[0])        # 找出当前Tag所处列表位置

            # 将相应Tag信息入列表
            list_time[tag_index].append(
                (int(tag_info[1]) - first_time) / 1000000)        # 对时间处理为精度0.1s
            list_rssi[tag_index].append(float(tag_info[2]))
            list_phase[tag_index].append(float(tag_info[3]))

    """粘合数据"""

    pos = [0 for i in range(0, len(list_epc))]
    upper_phase = [[] for i in range(0, len(list_epc))]
    upper_fit_phase = [[] for i in range(0, len(list_epc))]
    for i in range(0, len(list_epc)):
        upper_phase[i] = process(list_phase[i])
        [upper_fit_phase[i], pos[i]] = regression(list_time[i], upper_phase[i])
    colors = list(mcolors.TABLEAU_COLORS.keys())  # 颜色变化

    sorted_pos = sorted(enumerate(pos), key=lambda x: x[1])
    index = [i[0] for i in sorted_pos]
    pos = [i[1] for i in sorted_pos]
    plt.figure("order")
    print("order is " + str([list_epc[num][7:9] for num in index]))
    plt.title("order is " + str([list_epc[num][7:9] for num in index]))
    for i in range(0, len(list_epc)):
        plt.plot(list_time[i], upper_fit_phase[i],
                 color=mcolors.TABLEAU_COLORS[colors[i % 10]], marker='.', linestyle=':')
        plt.scatter(list_time[i], upper_phase[i],
                    color=mcolors.TABLEAU_COLORS[colors[i % 10]], marker='*')
    # list.sort(list_epc)
    plt.legend([num[7:9] for num in list_epc], loc='best',
               bbox_to_anchor=(0.77, 0.2), fontsize='small')   # 设置图例
    plt.savefig('./Super_V.png', dpi=600)
    plt.show()
