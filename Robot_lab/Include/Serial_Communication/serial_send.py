# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 3/30/2019 9:33 PM
# @Author: Yao ChengTao
# @File  : serial_send.py

import serial
import time

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

    def msg_to_hex(self, string):
        msgs = []
        for s in string:
            msgs.append(hex(s))
        print(msgs)
        return msgs

    def send_ready_cmd(self):
        self.port.write(self.start_cmd1)
        msg = self.port.readall()
        msg = self.msg_to_hex(msg)
        # time.sleep(1)
        self.port.write(self.start_cmd2)
        msg = self.port.readall()
        msg = self.msg_to_hex(msg)
        # if ( self.receive_msgs() == True ):
        #    self.port.write(self.start_cmd2)
        # msg = self.receive_msgs()

def test():
    go_cmd = [0xff, 0x00, 0x01, 0x01, 0x00, 0xa0, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00]

    robo_cmd = ser_command(com = 'COM3', baud = 115200)
    robo_cmd.send_ready_cmd()
    while True:
        robo_cmd.port.write(go_cmd)

if __name__=="__main__":
    test()
