# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 4/1/2019 10:09 AM
# @Author: Yao ChengTao
# @File  : draw_function.py

import math
import matplotlib.pyplot as plt


def plot_arrow(x, y, yaw, length=0.5, width=0.1):
    """
    plot arrow
    :param x: current position x
    :param y: current position y
    :param yaw: current yaw
    :param length: arrow length
    :param width: arrow width
    :return: None
    length_includes_head：determine whether arrow head length is included, default: False
    head_width：the width of the arrow head, default: 3*width
    head_length：the length of the arrow head, default: 1.5*head_width
    shape：param 'full'、'left'、'right' is shape of the arrow, default: 'full'
    overhang：代表箭头头部三角形底边与箭头尾部直接的夹角关系，通过该参数可改变箭头的形状。默认值为0，即头部为三角形，当该值小于0时，头部为菱形，当值大于0时，头部为鱼尾状
    """
    plt.arrow(x, y, length * math.cos(yaw), length * math.sin(yaw), head_length=1.5 * width, head_width=width)
    plt.plot(x, y)


def draw_trajectory(trajectory, x, goal, ob, is_dynamic, path = None):
    """
    :param trajectory: trajectory
    :param x: current or start position
    :param goal: goal
    :param ob: obstacle list
    :param is_dynamic: determine whether is dynamic
    :return: None
    """
    plt.cla()
    if is_dynamic:
        plt.plot(trajectory[:, 0], trajectory[:, 1], "-g")
    else:
        plt.plot(trajectory[:, 0], trajectory[:, 1], "-r")
    plt.plot(x[0], x[1], "xr")
    plt.plot(0, 0, "og")
    plt.plot(goal[0], goal[1], "or")
    plt.plot(ob[:, 0], ob[:, 1], "bs")
    plot_arrow(x[0], x[1], x[2])
    plt.axis("equal")
    if path is not None:
        plt.plot([path_point[0] for path_point in path], [path_point[1] for path_point in path], '-b')
    plt.grid(True)
    if is_dynamic:
        plt.pause(0.000001)
    else:
        plt.show()


def draw_path(path, x, goal, ob):

    plt.cla()
    plt.plot(x[0], x[1], "xr")
    plt.plot(0, 0, "og")
    plt.plot(goal[0], goal[1], "or")
    for (obstacle_x, obstacle_y, size) in ob:
        plt.plot(obstacle_x, obstacle_y, "sk", ms=10*size)
    plt.axis("equal")
    plt.plot([path_point[0] for path_point in path], [path_point[1] for path_point in path], '-b')
    plt.grid(True)
    plt.show()
