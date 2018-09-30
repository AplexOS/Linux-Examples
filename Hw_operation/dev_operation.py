#!/usr/bin/python3

import json
import serial
import threading
import time
import os

class Crc():
    def __init__(self):
        self.crc_result = 0xffff

    def ca_crc(self, data_array):
        self.crc_result = 0xffff
        for index in range(len(data_array) - 2):
            #print("0x%x" % data_array[index])

            self.crc_result ^= data_array[index]
            crc_num = (self.crc_result & 0x0001)
            for m in range(8):
                if crc_num :
                    xor_flag = 1;
                else:
                    xor_flag = 0

                self.crc_result >>= 1;

                if (xor_flag):
                    self.crc_result ^= 0xa001

                crc_num = (self.crc_result & 0x0001)


class dev_operation(Crc):
    def __init__(self, name, cfg, dev):
        self.name = name
        self.cfg = cfg
        self.ser = cfg.serial
        self.dev = dev

    def write_data_to_hw(self, slave_addr):
        #self.dev.read_data_cmd[0] = slave_addr

        self.ca_crc(self.dev.read_data_cmd)

        # ca crc
        self.dev.read_data_cmd[6] = (self.crc_result & 0xff)
        self.dev.read_data_cmd[7] = (self.crc_result >> 8)

        self.ser.write(self.dev.read_data_cmd)
        pass

    def read_data_from_hw(self):
        self.recvmsg = self.ser.read(self.dev.data_len)
        self.ser.reset_input_buffer()
        return self.recvmsg

    def operation(self, slave_addr):
        self.write_data_to_hw(slave_addr)
        #time.sleep(0.2)
        return self.read_data_from_hw()

    def set_dev_addr(self, slave_addr):
        self.dev.set_addr_cmd[4] = (slave_addr >> 8)
        self.dev.set_addr_cmd[5] = (slave_addr & 0xff)

        self.ca_crc(self.dev.set_addr_cmd)

        # ca crc
        self.dev.set_addr_cmd[6] = (self.crc_result & 0xff)
        self.dev.set_addr_cmd[7] = (self.crc_result >> 8)

        print(self.dev.set_addr_cmd)
        # set addr to device
        self.ser.write(self.dev.set_addr_cmd)

        # save new addr
        self.dev.addr = slave_addr
        pass


if __name__ == "__main__":
    print("main")

