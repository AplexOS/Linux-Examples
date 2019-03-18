#!/usr/bin/python3

import json
import serial
import threading
import time
import os
import sys
import math
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

class inclinometer():
    def __init__(self):
        self.config = config.config
        self.serial1_name = self.config["COM1"]["port"]
        self.serial_baudrate = self.config["COM1"]["baudrate"]
        self.timeout = self.config["COM1"]["timeout"]

        self.serial = serial.Serial(self.serial1_name, self.serial_baudrate, timeout = self.timeout)

        #self.lock = threading.Lock()
        self.lock = threading.Semaphore(5)

    def inclinometer_setaddr(self, old_addr=0x2, addr=0x3):
        self.incli_setaddr_cmd = [0x1, 0x06, 0x0, 0x7, 0x0, 0x0]

        self.incli_setaddr_cmd[0] = old_addr
        self.incli_setaddr_cmd[4] = addr
        self.incli_setaddr_cmd[5] = addr

        crc_num = ca_crc(self.incli_setaddr_cmd)

        self.incli_setaddr_cmd.append(crc_num & 0xff)
        self.incli_setaddr_cmd.append(crc_num >> 8)

        self.serial.write(self.incli_setaddr_cmd)

        self.incli_readaddr = self.serial.read(6)
        #print(self.incli_readaddr)

    def inclinometer_read(self, addr=0x2):
        incli_readdata_cmd =[0x1, 0x3, 0x0, 0x0, 0x0, 0x2]
        x_incli = -1

        incli_readdata_cmd[0] = addr

        crc_num = ca_crc(incli_readdata_cmd)

        incli_readdata_cmd.append(crc_num & 0xff)
        incli_readdata_cmd.append(crc_num >> 8)

        self.lock.acquire()
        self.serial.write(incli_readdata_cmd)
        #print(incli_readdata_cmd)

        time.sleep(0.05)
        try :
            incli_readdata = self.serial.read(9)
        except :
            self.lock.release()
            return -1
        else :
            self.lock.release()

        time.sleep(0.05)

        #print(incli_readdata)

        if (len(incli_readdata) > 5) :
            try :
                x_incli = (incli_readdata[3] * 100) \
                + incli_readdata[4] + (incli_readdata[5] / 100)
            except :
                print("read error")

        #return incli_readdata
        return x_incli

    def everage_value(self, addr=0x2):
        n = 0
        sum_result0 = []
        sum_result1 = []
        sum_result2 = []
        tmp_value = 0

        all_result = 0
        everage_val = 0

        while True :
            if (n == 20):
                break;

            tmp_value = self.security_read_incli_data(addr)
            if ((tmp_value >= 0) and (tmp_value <= 360)) :
                sum_result0.append(tmp_value)
                all_result = all_result + tmp_value
                n = n + 1
            else :
                continue

        everage_val = all_result / len(sum_result0)
        all_result = 0
        for i in range(len(sum_result0)) :
            if ((sum_result0[i] < (everage_val + 10)) and \
                    (sum_result0[i] > (everage_val - 10))):
                sum_result1.append(sum_result0[i])
                all_result = all_result + sum_result0[i]

        if (len(sum_result1) > 0) :
            everage_val = all_result / len(sum_result1)
            all_result = 0
            for i in range(len(sum_result1)) :
                if ((sum_result1[i] < (everage_val + 5)) and \
                        (sum_result1[i] > (everage_val - 5))):
                    sum_result2.append(sum_result1[i])
                    all_result = all_result + sum_result1[i]

            if (len(sum_result2)) :
                everage_val = all_result / len(sum_result2)

        return everage_val

    def security_read_incli_data(self, addr=0x2):
        result = -1
        n = 20
        while n :
            result = self.inclinometer_read(addr)

            if ((result < 0) or (result > 360)):
                n = n - 1
                result = -1
            else :
                break

        return result

class gps_sensor():
    def __init__(self):
        self.config = config.config
        self.serial2_name = self.config["COM2"]["port"]
        self.serial_baudrate = self.config["COM2"]["baudrate"]
        self.timeout = self.config["COM2"]["timeout"]

        self.serial = serial.Serial(self.serial2_name, self.serial_baudrate, timeout = self.timeout)

    def gps_get_data(self):

        self.data = {
                "e_longitude" : -1,
                "n_latitude" : -1
                }
        try :
            self.log_flag = 0
            tmp_data = self.serial.readline()
            tmp_gps_data = tmp_data.decode()

            gps_data_list = tmp_gps_data.split(',')

            if ((gps_data_list[0] == "$GNGLL") or (gps_data_list[0] == "$GPGLL")):
                if (gps_data_list[6] == "A"):
                    self.data["n_latitude"] = float(gps_data_list[1])
                    self.data["e_longitude"] = float(gps_data_list[3])
                    #self.log_flag = 1

            elif ((gps_data_list[0] == "$GNGGA") or (gps_data_list[0] == "$GNRMC") \
                    or (gps_data_list[0] == "$GPGGA")):
                if (gps_data_list[6] == "1"):
                    self.data["n_latitude"] = float(gps_data_list[2])
                    self.data["e_longitude"] = float(gps_data_list[4])
                    #self.log_flag = 1

            elif (gps_data_list[0] == "$GPRMC"):
                if (gps_data_list[2] == "A"):
                    self.data["n_latitude"] = float(gps_data_list[3])
                    self.data["e_longitude"] = float(gps_data_list[5])
                    #self.log_flag = 1

        except :
            #print("gps data get error")
            pass
        else :
            if (self.log_flag):
                logging.debug(tmp_data)

        return self.data;

    def filtrate_gps_data(self):
        n = 0

        while True:
            data = self.gps_get_data()
            if ((data["e_longitude"] < 13600) and (data["e_longitude"] > 7200)\
                    and (data["n_latitude"] > 200) and (data["n_latitude"] < 5400)):
                break

            n = n + 1

            if (n == 100):
                data["e_longitude"] = -1
                data["n_latitude"] = -1
                break

        return data

    def translate_min_to_point(self, num):
        minute = num % 100
        degress =  int(num / 100)

        return (degress + minute / 60)

    def security_get_gps_data(self):

        data = self.filtrate_gps_data()

        if ((data["e_longitude"] != -1) and (data["n_latitude"] != -1)):
            #print(data)
            data["e_longitude"] = self.translate_min_to_point(data["e_longitude"])
            data["n_latitude"] = self.translate_min_to_point(data["n_latitude"])

            result = self.wgs2gcj(data["n_latitude"], data["e_longitude"])
            #print(result)
            data["n_latitude"] = result[0]
            data["e_longitude"] = result[1]

        return data

    def read_gps_data_pthread(self):
        while True :
            self.serial.reset_input_buffer()
            gps_data = self.security_get_gps_data()
            config.e_longitude = gps_data["e_longitude"]
            config.n_latitude = gps_data["n_latitude"]
            time.sleep(1)

    def transformLat(self, lat,lon):
        ret = -100.0 + 2.0 * lat + 3.0 * lon + 0.2 * lon * lon + 0.1 * lat * lon +0.2 * math.sqrt(abs(lat))
        ret += (20.0 * math.sin(6.0 * lat * math.pi) + 20.0 * math.sin(2.0 * lat * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lon * math.pi) + 40.0 * math.sin(lon / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lon / 12.0 * math.pi) + 320 * math.sin(lon * math.pi  / 30.0)) * 2.0 / 3.0
        return ret

    #转换纬度
    def transformLon(self, lat, lon):
        ret = 300.0 + lat + 2.0 * lon + 0.1 * lat * lat + 0.1 * lat * lon + 0.1 * math.sqrt(abs(lat))
        ret += (20.0 * math.sin(6.0 * lat * math.pi) + 20.0 * math.sin(2.0 * lat * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * math.pi) + 40.0 * math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lat / 12.0 * math.pi) + 300.0 * math.sin(lat / 30.0 * math.pi)) * 2.0 / 3.0
        return ret

    #Wgs transform to gcj
    def wgs2gcj(self, lat, lon):
        a = 6378245.0
        ee = 0.00669342162296594323

        dLat = self.transformLat(lon - 105.0, lat - 35.0)
        dLon = self.transformLon(lon - 105.0, lat - 35.0)
        radLat = lat / 180.0 * math.pi
        magic = math.sin(radLat)
        magic = 1 - ee * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
        dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * math.pi)
        mgLat = lat + dLat
        mgLon = lon + dLon
        loc=[mgLat,mgLon]
        return loc

class sow_sensor():
    def __init__(self):
        self.config = config.config
        self.serial3_name = self.config["COM3"]["port"]
        self.serial_baudrate = self.config["COM3"]["baudrate"]
        self.timeout = self.config["COM3"]["timeout"]
        self.serial = serial.Serial(self.serial3_name, self.serial_baudrate, timeout = self.timeout)

        self.sow_result_old = []
        self.sow_result_old1 = []

        self.sow_data_last = [0, 0, 0, 0, 0]

        self.lock = threading.Semaphore(5)

        self.get_sow_data_start()

    def get_sow_data(self):
        sow_result = []
        count = 20

        #self.serial.reset_input_buffer()
        while count :
            try :
                sow_data = self.serial.read(17)
            except :
                continue
            else:
                pass

            if (len(sow_data) == 17) :
                sum = 0
                for i in range(15):
                    sum += sow_data[i]
                if ((sum & 0xff) != sow_data[15]):
                    continue
                sow_result.append(sow_data[4])
                sow_result.append(sow_data[5])
                sow_result.append(sow_data[6])

                sow_result.append((sow_data[7] << 24) + \
                        (sow_data[8] << 18) + \
                        (sow_data[9] << 8) + sow_data[10])

                sow_result.append((sow_data[11] << 24) + \
                        (sow_data[12] << 18) + \
                        (sow_data[13] << 8) + sow_data[14])

                break
            else:
                count = count - 1

        return sow_result

    def get_sow_data_start(self):
        get_sow_data_thread_1 = threading.Thread(target=self.get_sow_data_thread)
        get_sow_data_thread_1.start()

    def get_sow_data_thread(self):
        while True :
            tmp_data = self.get_sow_data()
            if (len(tmp_data) > 0) :
                self.sow_data_last = tmp_data

            time.sleep(0.5)

    def calculate_sow_data(self, flag):
        self.lock.acquire()
        sow_result_new = self.sow_data_last

        self.lock.release()
        if (flag == 0):
            if (len(sow_result_new) > 0) :
                if (len(self.sow_result_old) == 0):
                    self.sow_result_old = copy.deepcopy(sow_result_new)
                    return sow_result_new
                else :
                    #print(len(self.sow_result_old))
                    if (self.sow_result_old[3] > sow_result_new[3]) or \
                            (self.sow_result_old[4] > sow_result_new[4]) :
                        self.sow_result_old = copy.deepcopy(sow_result_new)
                        return sow_result_new
                    else :
                        sow_result = copy.deepcopy(sow_result_new)
                        sow_result[3] = sow_result_new[3] - self.sow_result_old[3]
                        sow_result[4] = sow_result_new[4] - self.sow_result_old[4]
                        self.sow_result_old = copy.deepcopy(sow_result_new)
                        return sow_result
            else :
                return [-1, -1, -1, -1, -1]
        elif (flag == 1):
            if (len(sow_result_new) > 0) :
                if (len(self.sow_result_old1) == 0):
                    self.sow_result_old1 = copy.deepcopy(sow_result_new)
                    return sow_result_new
                else :
                    #print(len(self.sow_result_old1))
                    if (self.sow_result_old1[3] > sow_result_new[3]) or \
                            (self.sow_result_old1[4] > sow_result_new[4]) :
                        self.sow_result_old1 = copy.deepcopy(sow_result_new)
                        return sow_result_new
                    else :
                        sow_result = copy.deepcopy(sow_result_new)
                        sow_result[3] = sow_result_new[3] - self.sow_result_old1[3]
                        sow_result[4] = sow_result_new[4] - self.sow_result_old1[4]
                        self.sow_result_old1 = copy.deepcopy(sow_result_new)
                        return sow_result
            else :
                return [-1, -1, -1, -1, -1]



if __name__ == "__main__":
    sow_test = sow_sensor()
    incli = inclinometer()

    while True :
        time.sleep(1)
        sow_data = sow_test.calculate_sow_data()
        print(sow_data)

        incli_data2 = incli.inclinometer_read(0x2)
        incli_data3 = incli.inclinometer_read(0x3)

        print(incli_data2)
        print(incli_data3)

