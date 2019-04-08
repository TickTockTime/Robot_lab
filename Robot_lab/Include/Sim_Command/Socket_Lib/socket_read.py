# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 4/9/2019 1:19 AM
# @Author: Yao ChengTao
# @File  : socket_read.py

"""
This module function to get information in Athena
"""

import socket
import Include.Sim_Command.Protocol_Lib.vision_detection_pb2 as vision_detection_pb2


def get_obstacle(id, isyellow, size):
    """
    This function is used to get obstacle information
    :param id: robot_id
    :param isyellow: is robot in yellow team
    :param size: size of obstacle
    :return: Obstacle list
    """
    ip_port = ('127.0.0.1', 23333)
    frame = vision_detection_pb2.Vision_DetectionFrame()
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sk.bind(ip_port)

    msg = sk.recv(4096)
    frame.ParseFromString(msg)
    obstacle = []

    if isyellow == True:
        for blue in frame.robots_blue:
            obstacle.append([blue.x / 10, blue.y / 10, size])
        for yellow in frame.robots_yellow:
            if yellow.robot_id != id:
                obstacle.append([yellow.x / 10, yellow.y / 10, size])
    else:
        for blue in frame.robots_blue:
            if blue.robot_id != id:
                obstacle.append([blue.x / 10, blue.y / 10, size])
        for yellow in frame.robots_yellow:
            obstacle.append([yellow.x / 10, yellow.y / 10, size])

    return obstacle


def get_position(id, isyellow):
    """
    This function is used to get robot position
    :param id: robot id
    :param isyellow: is robot in yellow team
    :return: position
    """
    ip_port = ('127.0.0.1', 23333)
    frame = vision_detection_pb2.Vision_DetectionFrame()
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sk.bind(ip_port)

    msg = sk.recv(4096)
    frame.ParseFromString(msg)
    position = []

    if isyellow == True:
        for yellow in frame.robots_yellow:
            if yellow.robot_id == id:
                position = [yellow.x / 10, yellow.y / 10, yellow.orientation]
    else:
        for blue in frame.robots_blue:
            if blue.robot_id == id:
                positon = [blue.x / 10, blue.y / 10, blue.orientation]

    return position


def test():
    """
    Test function
    :return: None
    """
    obstacle = get_obstacle(0, True, 20)
    position = get_position(0, True)
    print(obstacle)
    print(position)

if __name__ == "__main__":
    test()
