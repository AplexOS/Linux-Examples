#!/usr/bin/python3

import json
import serial
import threading
import time
import os
import sys
import logging
import copy

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

sys.path.append('../')
from Config.config import *

def ca_crc(data_array):
    crc_result = 0xffff
    for index in range(len(data_array)):
        #print("0x%x" % data_array[index])

        crc_result ^= data_array[index]
        crc_num = (crc_result & 0x0001)
        for m in range(8):
            if crc_num :
                xor_flag = 1;
            else:
                xor_flag = 0

            crc_result >>= 1;

            if (xor_flag):
                crc_result ^= 0xa001

            crc_num = (crc_result & 0x0001)

    return crc_result

class sensor():
    def __init__(self):
        self.config = config_data.config
        serial_name = self.config["COM1"]["port"]
        serial_baudrate = self.config["COM1"]["baudrate"]
        serial_timeout = self.config["COM1"]["timeout"]
        self.com = serial.Serial(serial_name, serial_baudrate, timeout = serial_timeout)

    def all_data(self, addr=0x1):
        read_all_data_cmd = [0x01, 0x03, 0x00, 0x0, 0x00, 0x09]

        read_all_data_cmd[0] = addr

        crc_num = ca_crc(read_all_data_cmd)

        read_all_data_cmd.append(crc_num >> 8)
        read_all_data_cmd.append(crc_num & 0xff)

        self.com.write(read_all_data_cmd)

        time.sleep(0.05)

        all_data = self.com.read(23)
        print(all_data)

    def co2_data(self, addr=0x1):
        read_co2_data_cmd = [0x01, 0x03, 0x00, 0x05, 0x00, 0x01]

        read_co2_data_cmd[0] = addr

        crc_num = ca_crc(read_co2_data_cmd)

        read_co2_data_cmd.append(crc_num >> 8)
        read_co2_data_cmd.append(crc_num & 0xff)

        self.com.write(read_co2_data_cmd)
        time.sleep(0.05)

        co2_data = self.com.read(7)


    def illumination_data(self, addr=0x1):
        read_ill_data_cmd = [0x01, 0x03, 0x00, 0x07, 0x00, 0x02]

        read_ill_data_cmd[0] = addr

        crc_num = ca_crc(read_ill_data_cmd)

        read_ill_data_cmd.append(crc_num >> 8)
        read_ill_data_cmd.append(crc_num & 0xff)

    def temperature_data(self, addr=0x1):
        read_temp_data_cmd = [0x01, 0x03, 0x00, 0x00, 0x00, 0x02]

        read_temp_data_cmd[0] = addr

        crc_num = ca_crc(read_temp_data_cmd)

        read_temp_data_cmd.append(crc_num >> 8)
        read_temp_data_cmd.append(crc_num & 0xff)

    def humidity_data(self, addr=0x1):
        read_humi_data_cmd = [0x01, 0x03, 0x00, 0x00, 0x00, 0x02]

        read_humi_data_cmd[0] = addr

        crc_num = ca_crc(read_humi_data_cmd)

        read_humi_data_cmd.append(crc_num >> 8)
        read_humi_data_cmd.append(crc_num & 0xff)

    def soil_ec(self):
        pass

    def soil_moisture_data(self):
        pass



