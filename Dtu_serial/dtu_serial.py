#!/usr/bin/python3

import serial
import threading
import time
import sys

sys.path.append("../")

from Dtu_dev.dtu_dev import *

class dtu_serial(threading.Thread) :
    def __init__(self, name, serial_com, flag):
        threading.Thread.__init__(self)
        self.name = name
        self.serial_com = serial_com
        self.flag = flag

    def msg_put_to_serial(self):
        while True :
            try :
                msg = dtu_dev.network_recv_queue.get(timeout=5)
                self.serial_com.write(msg)
                print("test serial write msg")
            except :
                print("serial write fial or queue timeout")

    def msg_get_from_serial(self):
        while True :
            try :
                msg = self.serial_com.read(128)
                print("serial read len : %d" % len(msg))
                dtu_dev.network_send_queue.put(msg)
            except :
                print("serial read fail")

    def run(self):
        if (self.flag) :
            self.msg_put_to_serial()
        else :
            self.msg_get_from_serial()

