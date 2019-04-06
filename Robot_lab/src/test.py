# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 4/1/2019 9:36 AM
# @Author: Yao ChengTao
# @File  : test.py

import math
import numpy as np
import Include.Planner.extra_rapidly_exploring_random_tree as errt
import Include.Planner.dynamic_window_approach as dwa
import Include.Sim_Command.SocketRead as read
import Include.Serial_Communication.serial_send as send

map_info = read.socket_read()
obstacle = map_info.get_obstacle()
obstacle = np.array(obstacle)
start_position = map_info.get_position()
start = [start_position[0], start_position[1]]
print(start)

"""
obstacle = np.array([[5, 1, 1],
            [3, 6, 2],
            [3, 8, 2],
            [1, 1, 2],
            [3, 5, 2],
            [9, 5, 2],
            [3, 0, 3]])

ob = np.array([[5, 1],[3, 6],[3, 8],[1, 1],[3, 5],[9, 5],[3, 0]])
"""

errt_plan = errt.ERRT_Plan(start = start, goal = [-240, 170],  obstacle = obstacle, map_scope=[-250, 250, -180, 180])
path = errt_plan.errt_planning()
print(path)

robo_cmd = send.ser_command(com = 'COM3', baud = 115200)
robo_cmd.send_ready_cmd()


x = [start_position[0], start_position[1], start_position[2], 100, 0.0, 0.0]
u = [100, 0.0, 0.0]
for i in range(len(path)-1):
    # print([path[i+1][0],path[i+1][1]])
    x = dwa.dynamic_windwo_approach(x, u, goal=[path[i+1][0],path[i+1][1]], ob=obstacle, path=path, id=1, serial=robo_cmd)
    u = [x[3], x[4], x[5]]
