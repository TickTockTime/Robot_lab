# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 3/30/2019 9:33 PM
# @Author: Yao ChengTao
# @File  : serial_send.py

import serial
import math
import Include.Serial_Communication.command_generate as cmd

class ser_command(object):
    """
    :param object: com port and the baud
    :return: None
    """

    def __init__(self, com, baud):
        self.com = com
        self.baud = baud
        self.port = serial.Serial(self.com, self.baud, bytesize=8, stopbits=2, timeout=0.1)
        self.start_cmd1 = [0xff,0xb0,0x01,0x02,0x03,0x00,0x00,0x00,
                           0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                           0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x31]
        self.start_cmd2 = [0xff,0xb0,0x04,0x05,0x06,0x10,0x00,0x00,
                           0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                           0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x85]

    def send_cmd(self, cmd):
        self.port.write(cmd)
        msg = self.port.readall()
        msg = self.msg_to_hex(msg)
        print(msg)


    def msg_to_hex(self, string):
        msgs = []
        for s in string:
            msgs.append(hex(s))
        return msgs

    def send_ready_cmd(self):
        self.port.write(self.start_cmd1)
        msg = self.port.readall()
        msg = self.msg_to_hex(msg)
        print(msg)
        # time.sleep(1)
        self.port.write(self.start_cmd2)
        msg = self.port.readall()
        msg = self.msg_to_hex(msg)
        print(msg)
        # if ( self.receive_msgs() == True ):
        #    self.port.write(self.start_cmd2)
        # msg = self.receive_msgs()

def test():
    """
    go_cmd = [0xff, 0x00, 0x02, 0x01, 0x00, 0xa0, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00]
    """
    go_cmd = cmd.command_raw(1,10,0, -180*math.pi/180)

    robo_cmd = ser_command(com = 'COM3', baud = 115200)
    robo_cmd.send_ready_cmd()
    while True:
        robo_cmd.send_cmd(go_cmd)

if __name__=="__main__":
    test()
