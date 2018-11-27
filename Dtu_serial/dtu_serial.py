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
            if(dtu_dev.network_recv_queue.empty()) :
                time.sleep(3)
            else :
                msg = dtu_dev.network_recv_queue.get()
                self.serial_com.write(msg)
                print("test serial write msg")
                #time.sleep(3)

    def msg_get_from_serial(self):
        while True :
            msg = self.serial_com.read(128)
            print("serial read len : %d" % len(msg))
            dtu_dev.network_send_queue.put(msg)

    def run(self):
        if (self.flag) :
            self.msg_put_to_serial()
        else :
            self.msg_get_from_serial()

