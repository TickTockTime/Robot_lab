# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 4/1/2019 9:36 AM
# @Author: Yao ChengTao
# @File  : test.py

import math
import numpy as np
import Include.Planner.extra_rapidly_exploring_random_tree as errt
import Include.Planner.dynamic_window_approach as dwa

obstacle = [[5, 1, 1],
            [3, 6, 2],
            [3, 8, 2],
            [1, 1, 2],
            [3, 5, 2],
            [9, 5, 2],
            [3, 0, 3]]

ob = np.array([[5, 1],[3, 6],[3, 8],[1, 1],[3, 5],[9, 5],[3, 0]])

errt_plan = errt.ERRT_Plan(start=[0, 0], goal=[8, 10], map_scope=[-2, 10, -2, 10], obstacle=obstacle)
path = errt_plan.errt_planning()

x = [path[0][0], path[0][1], math.pi/2.0, 0.2, 0.0, 0.0]
u = [0.2, 0.0, 0.0]
for i in range(len(path)-1):
    # print([path[i+1][0],path[i+1][1]])
    x = dwa.dynamic_windwo_approach(x, u, goal=[path[i+1][0],path[i+1][1]], ob=ob, path=path)
    u = [x[3], x[4], x[5]]
