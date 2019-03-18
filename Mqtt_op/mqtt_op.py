#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time
import json
import threading
import math
import sys
import queue
import copy
import logging

sys.path.append('../')
from Config.config import *
from Sensor_op.sensor_op import *
from Sqlite_op.dtu_sqlite import *
from Upgrade.upgrade import *

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

class mqtt_operation(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        #self.__mutex = threading.Lock()
        self.__mutex = threading.Semaphore()
        self.__name = name
        self.config = config.config
        self.config_device = config.config_device

        self.incli = inclinometer()
        self.gps = gps_sensor()
        self.sow = sow_sensor()
        self.incli_data0 = -1
        self.incli_data1 = -1

        self.is_connect_flag = 0
        self.is_start_pubmsg_flag = 0

        #self.message_queue = queue.Queue(maxsize = 2048 * 1024)
        self.sql_op = dtu_sqlite()

        self.sql_op.create_tables("database0.db")
        self.sql_op.create_tables("database1.db")

        self.pub1 = "emi/iot/tractors/server"

        self.message = {
                "apiCode":61002,
                "data" :{
                    "device_id" :"-1",
                    "e_longitude" : -1,
                    "n_latitude" : -1,
                    "created" : "2018-12-20 14:00:00",
                    "is_work" : 0,
                    "user_id" : "-1",
                    "land_id" : "-1",
                    "width" : 0,
                    "farmSet" : 1,
                    "len_angle0" : -1,
                    "len_angle1" : -1,
                    "elev_angle" : -1,
                    "version" : "1.0.0",
                    "content" :{
                        "seed_of_row1" : -1,
                        "seed_of_row2" : -1,
                        "col_space" : -1,
                        "row_num" : -1,
                        "row_space" : -1
                        }
                    }
                }
        self.message["data"]["version"] = self.config["version"]

        self.gps_data = {
                "e_longitude" : -1,
                "n_latitude" : -1
                }

        self.init_connect()

    def init_connect(self):
        self.__mutex.acquire()
        self.__mqtt_id = str(math.floor(time.time()))
        self.__mqtt__ = mqtt.Client(self.__mqtt_id)
        self.__mqtt__.username_pw_set(self.config["mqtt"]["username"], self.config["mqtt"]["passwd"])
        self.__mqtt__.on_connect = self.on_connect
        self.__mqtt__.on_disconnect = self.on_disconnect
        self.__mqtt__.on_message = self.recvmsg_from_mqtthub

        self.__mutex.release()

        self.try_connect_to_mqtthub()

    def on_connect(self, client, userdata, flags, rc):
        try :
            client.subscribe("emi/iot/tractors/client/device/" + self.config["device"]["id"])
            message = {
                    "apiCode" : 61001,
                    "data" : {
                        "device_id" : "-1",
                        "version" : "1.0.0"
                        }
                    }

            message["data"]["version"] = self.config["version"]

            message["data"]["device_id"] = self.config["device"]["id"]
            self.__mqtt__.publish(self.pub1, payload = json.dumps(message), retain = False)

        except :
            logging.debug("subscribe error")
        else :
            logging.debug("subscribe ok....")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logging.debug("disconect start")
            self.is_connect_flag = 0
            self.try_connect_to_mqtthub()
            logging.debug("disconect stop")
            time.sleep(2)

    def try_connect_to_mqtthub(self):
        while True :
            try :
                logging.debug("connect start")
                self.__mqtt__.connect(self.config["mqtt"]["wss_addr"], self.config["mqtt"]["wss_port"], keepalive=10)
            except :
                logging.debug("connect error")
                time.sleep(2)
            else :
                self.is_connect_flag = 1
                logging.debug("connect success")
                break

    def recvmsg_from_mqtthub(self, client, userdata, msg):
        try :
            json_data = json.loads(msg.payload.decode('utf8'))
            logging.debug(json_data)

        except :
            logging.debug("decode msg error")
        else:
            if (("apiCode" in json_data) and \
                    ("data" in json_data)) :
                if (json_data["apiCode"] == 66001):
                    logging.debug("update .....")
                    self.recv_sensor_update_data(json_data["data"])

                elif (json_data["apiCode"] == 66002):
                    self.recv_sensor_time_data(json_data["data"])

                elif (json_data["apiCode"] == 66003):
                    self.recv_sensor_width_data(json_data["data"])

                elif (json_data["apiCode"] == 66004):
                    self.recv_sensor_user_id_data(json_data["data"])

                elif (json_data["apiCode"] == 66005):
                    self.recv_sensor_land_id_data(json_data["data"])

                elif (json_data["apiCode"] == 66006):
                    self.recv_sensor_interval_data(json_data["data"])

                elif (json_data["apiCode"] == 66007):
                    self.recv_anglethreshold_data(json_data["data"])

    def pub_ack_data(self, apicode, returnText):
        self.ack = {
            "apiCode" : 61003,
            "data" : {
                "device_id" : "-1",
                "message" : {
                    "apiCode": 66001,
                    "returnCode" : "SUCCESS",
                    "returnText" : "操作成功"
                    }
                }
            }

        self.ack["data"]["device_id"] = self.config["device"]["id"]
        self.ack["data"]["message"]["apiCode"] = apicode
        self.ack["data"]["message"]["returnText"] = returnText

        try :
            self.__mqtt__.publish(self.pub1, payload = json.dumps(self.ack), retain = False)

            topical = "emi/iot/tractors/client/user/" + \
                    self.config_device["device"]["user_id"] + "/alltomap"
            self.__mqtt__.publish(topical, payload=json.dumps(self.ack), retain = False)
        except :
            logging.debug("recv ack error")

        if ((apicode == 66001) or (apicode == 66003)\
                or (apicode == 66004) or (apicode == 66005)) :
            config.save_config_device_data()
        else :
            config.save_config_data()

    def recv_sensor_update_data(self, update_data):
        if "update" in update_data :
            if (update_data["update"] == "true"):
                ftp_update = ftp_upgrade()
                ftp_update.auto_download()
                ftp_update.auto_update()

            self.pub_ack_data(66001, "操作成功")
            os.system("reboot")

    def recv_sensor_time_data(self, time_data):
        if "created" in time_data:
            date_cmd = "date -s \"" + time_data["created"] + "\""
            os.system(date_cmd)
            os.system("hwclock -w")

            if (not self.is_start_pubmsg_flag):
                self.send_msg_threads()

            self.is_start_pubmsg_flag = 1
            self.pub_ack_data(66002, "操作成功")

    def recv_sensor_width_data(self, width_data):
        if "width" in width_data:
            self.config_device["device"]["width"] = width_data["width"]
            self.message["data"]["farmSet"] = 1
            self.pub_ack_data(66003, "操作成功")

    def recv_sensor_user_id_data(self, user_id_data):
        if "user_id" in user_id_data:
            self.config_device["device"]["user_id"] = user_id_data["user_id"]
            self.pub_ack_data(66004, "操作成功")

    def recv_sensor_land_id_data(self, land_id_data):
        if "land_id" in land_id_data:
            self.config_device["device"]["land_id"] = land_id_data["land_id"]
            self.pub_ack_data(66005, "操作成功")

    def recv_sensor_interval_data(self, interval_data):
        flag = 0

        if "interval" in interval_data:
            self.config["device"]["interval"] = interval_data["interval"]
            flag = 1

        if "intervalUser" in interval_data:
            self.config["device"]["intervalUser"] = interval_data["intervalUser"]
            flag = 1

        if flag :
            self.pub_ack_data(66006, "操作成功")

    def recv_anglethreshold_data(self, angleThreshold_data):
        if "angleThreshold" in angleThreshold_data :
            self.config["device"]["angleThreshold"] = angleThreshold_data["angleThreshold"]
            self.pub_ack_data(66007, "操作成功")

    def send_msg_threads(self):
        gps_read_thread = threading.Thread(target=self.gps.read_gps_data_pthread)
        gps_read_thread.start()

        send_message_thread0 = threading.Thread(target=self.send_message_to_server)
        send_message_thread0.start()

        get_incli_data_thread0 = threading.Thread(target=self.get_incli_pthread)
        get_incli_data_thread0.start()

        send_message_thread1 = threading.Thread(target=self.send_message_to_tractors)
        send_message_thread1.start()

        clear_data_thread0 = threading.Thread(target=self.clear_sqlite_data, args=["database0.db",])
        clear_data_thread0.start()

        clear_data_thread1 = threading.Thread(target=self.clear_sqlite_data, args=["database1.db",])
        clear_data_thread1.start()

    def compile_message(self, message):
        message["data"]["device_id"] = self.config["device"]["id"]
        message["data"]["width"] = self.config_device["device"]["width"]
        message["data"]["created"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        message["data"]["user_id"] = self.config_device["device"]["user_id"]
        message["data"]["land_id"] = self.config_device["device"]["land_id"]
        message["data"]["width"] = self.config_device["device"]["width"]

        incli_data0 = self.incli_data0
        incli_data1 = self.incli_data1

        cmp_value = incli_data1 - incli_data0
        message["data"]["is_work"] = 1
        if ((incli_data0 < 180) and (cmp_value > 90)):
            message["data"]["elev_angle"] = cmp_value - 180
            if (message["data"]["elev_angle"] >= self.config["device"]["angleThreshold"]):
                message["data"]["is_work"] = 0

        elif((incli_data0 < 180) and (cmp_value < 90)):
            message["data"]["elev_angle"] = cmp_value - 0
            if (message["data"]["elev_angle"] <= (self.config["device"]["angleThreshold"] * -1)):
                message["data"]["is_work"] = 0
            message["data"]["elev_angle"] = message["data"]["elev_angle"] * -1

        elif((incli_data0 > 180) and (cmp_value < -90)):
            message["data"]["elev_angle"] = cmp_value + 180
            if (message["data"]["elev_angle"] <= (self.config["device"]["angleThreshold"] * -1)):
                message["data"]["is_work"] = 0
            message["data"]["elev_angle"] = message["data"]["elev_angle"] * -1

        elif((incli_data0 > 180) and (cmp_value > -90)):
            message["data"]["elev_angle"] = cmp_value - 0
            if (message["data"]["elev_angle"] >= self.config["device"]["angleThreshold"]):
                message["data"]["is_work"] = 0

        logging.debug("incli0 : " + str(incli_data0) + "  incli1 : " + str(incli_data1) + "  elev_angle : " + str(message["data"]["elev_angle"]))

        message["data"]["len_angle0"] = incli_data0
        message["data"]["len_angle1"] = incli_data1

        message["data"]["e_longitude"] = config.e_longitude
        message["data"]["n_latitude"] = config.n_latitude

    def send_message_to_tractors(self):

        continue_flag = 0

        while True :
            self.tractor_message_pub = copy.deepcopy(self.message)
            self.compile_message(self.tractor_message_pub)

            self.tractors_pub = "emi/iot/tractors/client/user/" + \
                    self.config_device["device"]["user_id"] + "/alltomap"

            if (self.tractor_message_pub["data"]["is_work"] == 1):
                del self.tractor_message_pub["data"]["content"]
                cur_qos = 0
                continue_flag = 0

            elif (self.tractor_message_pub["data"]["is_work"] == 0):
                if(not continue_flag) :
                    sow_data = self.sow.calculate_sow_data(0)

                    self.tractor_message_pub["data"]["content"]["seed_of_row1"] = sow_data[3]
                    self.tractor_message_pub["data"]["content"]["seed_of_row2"] = sow_data[4]
                    self.tractor_message_pub["data"]["content"]["col_space"] = sow_data[0]
                    self.tractor_message_pub["data"]["content"]["row_num"] = sow_data[1]
                    self.tractor_message_pub["data"]["content"]["row_space"] = sow_data[2]
                    cur_qos = 2

                if (continue_flag):
                    del self.tractor_message_pub["data"]["content"]

            if (self.is_connect_flag):
                try :
                    rc = self.__mqtt__.publish(self.tractors_pub, \
                            payload = json.dumps(self.tractor_message_pub), \
                            qos = cur_qos, retain = False)
                except :
                    self.sql_op.insert_data(self.tractor_message_pub, "database0.db")
                    logging.debug("insert data")
                else :
                    if (rc[0] > 0):
                        self.sql_op.insert_data(self.tractor_message_pub, "database0.db")
                        logging.debug("insert data")
            else :
                self.sql_op.insert_data(self.tractor_message_pub, "database0.db")
                logging.debug("insert data")

            if (self.tractor_message_pub["data"]["is_work"] == 0):
                continue_flag = 1

            time.sleep(self.config["device"]["intervalUser"])

    def get_incli_pthread(self):
        while True :
            #self.incli_data0 = self.incli.security_read_incli_data(0x3)
            #self.incli_data1 = self.incli.security_read_incli_data(0x4)

            self.incli_data0 = self.incli.everage_value(0x4)
            self.incli_data1 = self.incli.everage_value(0x3)

            logging.debug(self.incli_data0)
            logging.debug(self.incli_data1)
            time.sleep(0.5)

    def send_message_to_server(self):
        conut_number = 0
        last_is_work_status = 0

        while True :
            self.server_message_pub = copy.deepcopy(self.message)
            self.compile_message(self.server_message_pub)

            self.server_pub = "emi/iot/tractors/server"

            if (self.server_message_pub["data"]["is_work"] == 1):

                del self.server_message_pub["data"]["content"]
                cur_qos = 0

                last_is_work_status = 1

            elif (self.server_message_pub["data"]["is_work"] == 0):
                if (last_is_work_status == 1) :
                    sow_data = self.sow.calculate_sow_data(1)

                    self.server_message_pub["data"]["content"]["seed_of_row1"] = sow_data[3]
                    self.server_message_pub["data"]["content"]["seed_of_row2"] = sow_data[4]
                    self.server_message_pub["data"]["content"]["col_space"] = sow_data[0]
                    self.server_message_pub["data"]["content"]["row_num"] = sow_data[1]
                    self.server_message_pub["data"]["content"]["row_space"] = sow_data[2]
                    cur_qos = 2
                else :
                    del self.server_message_pub["data"]["content"]

                last_is_work_status = 0

            if (self.is_connect_flag):
                try :
                    #logging.debug(self.server_message_pub["data"]["len_angle0"])
                    #logging.debug(self.server_message_pub["data"]["len_angle1"])

                    rc = self.__mqtt__.publish(self.server_pub, \
                            payload = json.dumps(self.server_message_pub), \
                            qos = cur_qos, retain = False)
                except :
                    self.sql_op.insert_data(self.server_message_pub, "database1.db")
                    loggind.debug("insert data")
                else :
                    if (rc[0] > 0):
                        self.sql_op.insert_data(self.server_message_pub, "database1.db")
                        logging.debug("insert data")
            else :
                self.sql_op.insert_data(self.server_message_pub, "database1.db")
                logging.debug("insert data")

            time.sleep(self.config["device"]["interval"])

    def clear_sqlite_data(self, database_name):
        while True :
            if (self.is_connect_flag) :
                temp_msgs = None
                temp_msgs = self.sql_op.print_all_data(database_name)

                for data in temp_msgs:
                    #print(data)
                    if (len(data) > 0):
                        if (database_name == "database1.db"):
                            topical = "emi/iot/tractors/server"
                        elif (database_name == "database0.db"):
                            topical = "emi/iot/tractors/client/user/" \
                                    + self.config_device["device"]["user_id"] \
                                    + "/alltomap"
                        try :
                            self.__mqtt__.publish(topical, payload=data, retain = False)
                        except :
                            self.sql_op.insert_data(self.server_message_pub, database_name)
                            logging.debug("publish queue msg error and insert data to database")
                            time.sleep(2)

                time.sleep(5)

            else :
                time.sleep(10)

    def run(self):
        self.__mqtt__.loop_forever()

if __name__ == "__main__" :
    mqtt_operation = mqtt_operation("mqtt_main_thread")
    mqtt_operation.start()
    mqtt_operation.join()


