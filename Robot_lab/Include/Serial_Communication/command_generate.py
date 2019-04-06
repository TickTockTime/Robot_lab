# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 4/4/2019 3:54 PM
# @Author: Yao ChengTao
# @File  : command_generate.py

import math

def command_generate(robot_id, vx, vy, w):

    cmd = [0xff, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
           0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00]

    if robot_id >= 8:
        cmd[1] = 0x01 << (robot_id - 8)
    else:
        cmd[2] = 0x01 << robot_id


    if vx < 0:
        cmd[4] = cmd[4] | (0x20)
    cmd[4] = cmd[4] | ((abs(vx) & 0x1f0) >> 4)
    cmd[5] = cmd[5] | ((abs(vx) & 0x0f) << 4)

    if vy < 0:
        cmd[5] = cmd[5] | (0x08)
    cmd[5] = cmd[5] | ((abs(vy) & 0x1c0) >> 6)
    cmd[6] = cmd[6] | ((abs(vy) & 0x3f) << 2)

    if w < 0:
        cmd[6] = cmd[6] | (0x02)
    cmd[6] = cmd[6] | ((abs(w) & 0x100) >> 8)
    cmd[7] = cmd[7] | (abs(w) & 0x0ff)
    command = [hex(i) for i in cmd]
    print(command)
    return cmd

def command_raw(robot_id, v, w, orientation):
    # v = int(v)
    cmd = command_generate(robot_id, int(v*math.cos(orientation)), int(v*math.sin(orientation)), int(40*w))
    return cmd

def main():
    cmd = command_raw(1,1,0,1)
    print(cmd)

if __name__=="__main__":
    main()
