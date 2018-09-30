#!/usr/bin/python3

import time
import json
import threading
import math
import sys

sys.path.append('../')
from Config.config import *
from Slave_dev.slave_dev import *
from Hw_operation.dev_operation import *
from Rainfull_dev.rainfull_dev import *

class hw_data():
    def __init__(self):
        self.send_msg = {
            "d":
            [
                {
                    "t":"temp_data",
                    "v":-1,
                    "q":0
                },
                {
                    "t":"humi_data",
                    "v":-1,
                    "q":0
                },
                {
                    "t":"illumination_data",
                    "v":-1,
                    "q":0
                },
                {
                    "t":"co2_data",
                    "v":-1,
                    "q":0
                },
                {
                    "t":"soil_moisture_data",
                    "v":-1,
                    "q":0
                },
                {
                    "t":"pressuer_data",
                    "v":-1,
                    "q":0
                },
                {
                    "t":"rainfall_data",
                    "v":-1,
                    "q":0
                }
            ],
            "ts":"2017-12-22T08:05:20+ 0000"
        }

        self.rainfull_dev = rainfull()

        # slave device operation
        temp_dev = Temp_humi_dev()
        self.temp_slave_operation = dev_operation("temp_dev", config, temp_dev)

        illumination_dev = Illumination_detect()
        self.illumination_slave_operation = dev_operation("light_dev", config, illumination_dev)

        co2_dev = Co2_detect()
        self.co2_slave_operation = dev_operation("co2_dev", config, co2_dev)

        soil_dev = Soil_moisture_detect()
        self.soil_slave_operation = dev_operation("soil_dev", config, soil_dev)

        pressure_dev = Pressure_detect()
        self.pressure_slave_operation = dev_operation("case_dev", config, pressure_dev)

    def get_hw_data(self):
        self.send_msg["d"][6]["v"] = self.rainfull_dev.rain_data
        self.rainfull_dev.rain_data = 0

        self.temp_data = self.temp_slave_operation.operation(0x1)
        self.illu_data = self.illumination_slave_operation.operation(0x1)
        self.co2_data  = self.co2_slave_operation.operation(0x1)
        self.soil_data = self.soil_slave_operation.operation(0x1)
        self.pres_data = self.pressure_slave_operation.operation(0x1)

        if (len(self.temp_data) >= 5) :
            self.send_msg["d"][0]["v"] = (((self.temp_data[3] << 8) + self.temp_data[4]) / 10)
            self.send_msg["d"][1]["v"] = (((self.temp_data[5] << 8) + self.temp_data[6]) / 10)

        if (len(self.illu_data) >= 7) :
            self.send_msg["d"][2]["v"] = ((self.illu_data[3] << 24) + (self.illu_data[4] << 16) + (self.illu_data[5] << 8) + self.illu_data[6])

        if (len(self.co2_data) >= 5) :
            self.send_msg["d"][3]["v"] = ((self.co2_data[3] << 8) + self.co2_data[4])

        if (len(self.soil_data) >= 5) :
            self.send_msg["d"][4]["v"] = (((self.soil_data[3] << 8) + self.soil_data[4]) / 10)

        if (len(self.pres_data) >= 5) :
            self.send_msg["d"][5]["v"] = (((self.pres_data[3] << 8) + self.pres_data[4]) / 1000)

        self.send_msg["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S+ 0800", time.localtime())

