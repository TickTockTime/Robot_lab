# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 4/9/2019 1:13 AM
# @Author: Yao ChengTao
# @File  : socket_control.py


"""
This module send control command to Athena
"""

import math
import socket
import Include.Sim_Command.Protocol_Lib.grSim_Packet_pb2 as grSim_Packet_pb2


def control(robot_id, isyellow, v, w, orientation):
    """
    This function is used to generate and send the control command
    :param robot_id: robot_id
    :param isyellow: is robot in yellow team
    :param v: vel
    :param w: velangular
    :param orientation: vel orientation
    :return: None
    """
    girsim_packet = grSim_Packet_pb2.grSim_Packet()
    girsim_packet.commands.timestamp = 0.1
    girsim_packet.commands.isteamyellow = isyellow
    control_cmd = girsim_packet.commands.robot_commands.add()
    control_cmd.id = robot_id
    control_cmd.kickspeedx = 0
    control_cmd.kickspeedz = 0
    control_cmd.veltangent = v * math.cos(orientation)
    control_cmd.velnormal = v * math.sin(orientation)
    control_cmd.velangular = w
    control_cmd.spinner = False
    control_cmd.wheelsspeed = False

    address = ('127.0.0.1', 20011)
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.sendto(girsim_packet.SerializeToString(), address)


def test():
    """
    Test function
    :return: None
    """
    robot_id = 3
    isyellow = False
    v = 0
    w = - 720 * math.pi / 180
    orientation = 45 * math.pi / 180
    control(robot_id, isyellow, v, w, orientation)


if __name__ == "__main__":
    test()
