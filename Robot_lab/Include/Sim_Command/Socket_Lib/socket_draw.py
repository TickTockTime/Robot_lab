# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 4/9/2019 12:49 AM
# @Author: Yao ChengTao
# @File  : socket_draw.py

"""
This module contains some functions to draw in Athena
"""

import socket
import Include.Sim_Command.Protocol_Lib.zss_debug_pb2 as zss_debug_pb2


def draw_line(packet, start, end, color):
    """
    This function is used to draw line in Athena
    :param packet: protocol buffer message
    :param start: start point
    :param end: end point
    :param color: line color
    :return: None
    """
    msg = packet.msgs.add()
    msg.type = 1
    msg.color = color
    msg.line.start.x = start[0]
    msg.line.start.y = start[1]
    msg.line.end.x = end[0]
    msg.line.end.y = end[1]
    msg.line.FORWARD = True
    msg.line.BACK = True


def draw_rectangle(packet, start, end, color):
    """
    This function is used to draw rectangle in Athena
    :param packet: protocol buffer message
    :param start: top-left point
    :param end: bottom right point
    :param color: line color
    :return: None
    """
    draw_line(packet, start, [end[0], start[1]], color)
    draw_line(packet, [end[0], start[1]], end, color)
    draw_line(packet, end, [start[0], end[1]], color)
    draw_line(packet, [start[0], end[1]], start, color)


def draw_path(packet, path, color):
    """
    This function is used to draw path in Athena
    :param packet: protocol buffer message
    :param path: path
    :param color: line color
    :return: None
    """
    for i in range(len(path)-1):
        draw_line(packet, path[i], path[i+1], color)


def send_draw_command(packet):
    """
    This function is used to send command to Athena
    :param packet: protocol buffer message
    :return: None
    """
    address = ('127.0.0.1', 20001)
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.sendto(packet.SerializeToString(), address)


def test():
    """
    Test function to test
    color number:
        0   white
        1   red
        2   orange
        3   yellow
        4   green
        5   cyan
        6   blue
        7   purple
        8   gray
        9   black
    :return: None
    """
    color = 0
    draw = zss_debug_pb2.Debug_Msgs()
    path = [[-12, 2],
            [15, 7],
            [20, -30],
            [100, -180]]

    draw_line(draw, [2, 2], [100, 100], color)
    draw_rectangle(draw, [-2, -2], [-100, -100], color)
    draw_path(draw, path, color)

    send_draw_command(draw)


if __name__ == "__main__":
    test()
