#!/usr/bin/python3

import paho.mqtt.client as mqtt
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
from Hw_data.hw_data import *

class mqtt_operation(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.__mutex = threading.Lock()
        self.__name = name
        self.config = config
        self.serial = config.serial
        self.init_connect()

    def init_connect(self):
        self.__mutex.acquire()
        self.__mqtt_id = str(math.floor(time.time()))
        self.__mqtt__ = mqtt.Client(self.__mqtt_id)
        #self.__mqtt__.username_pw_set(self.config["mqtt"]["username"], self.config["mqtt"]["passwd"])
        self.__mqtt__.on_connect = self.on_connect
        self.__mqtt__.on_disconnect = self.on_disconnect
        self.__mqtt__.on_message = self.recvmsg_from_mqtthub
        self.__mutex.release()

        self.try_connect_to_mqtthub()

    def on_connect(self, client, userdata, flags, rc):
        try :
            client.subscribe("/cloud/account1/accountType1/5243197/command2c")
            pass
        except :
            #print("subscribe error")
            pass
        else :
            #print("subscribe ok")
            pass

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("disconect start")
            self.try_connect_to_mqtthub()
            print("disconect stop")
            time.sleep(2)

    def try_connect_to_mqtthub(self):
        while True :
            try :
                print("connect start")
                self.__mqtt__.connect(self.config.config["mqtt"]["wss_addr"], 5006)
            except :
                print("connect error")
                time.sleep(2)
            else :
                print("connect success")
                break

    def recvmsg_from_mqtthub(self, client, userdata, msg):
        chat = "/cloud/account1/accountType1/5243197/command2s"
        ack = {
            "c2c":
            {
                "ssid":"kjdfafiuwerfoiuqer0298r09uu0euf98fu",
                "sqid":"1234567890",
                "opid":"set.conf1.Report.ack",
                "param":
                [
                    {
                    "t":"return",
                    "v":"ok"
                    }
                ]
            }
        }
        try :
            json_data = json.loads(msg.payload.decode('utf8'))
        except :
            ack["c2c"]["param"][0]["v"] = "error"
        else:
            if ("c2c" in json_data) :
                event = json_data["c2c"]["param"][0]["v"]
                value = json_data["c2c"]["param"][1]["v"]
                unit = json_data["c2c"]["param"][2]["v"]

                if (unit == "ms") :
                    config.config["sensor"]["timing"] = (value / 1000)
                elif (unit == "s") :
                    config.config["sensor"]["timing"] = value
                elif (unit == "m") :
                    config.config["sensor"]["timing"] = (value * 60)
                elif (unit == "h") :
                    config.config["sensor"]["timing"] = (value * 60 * 60)
                elif (unit == "d") :
                    config.config["sensor"]["timing"] = (value * 60 * 60 * 24)

                try :
                    with open("Config/config.json", "w") as config_file :
                        config_file.write(json.dumps(config.config))
                except :
                    with open("../Config/config.json", "w") as config_file :
                        config_file.write(json.dumps(config.config))

                ack["c2c"]["param"][0]["v"] = "ok"
            else :
                ack["c2c"]["param"][0]["v"] = "error"


        self.__mqtt__.publish(chat, payload = json.dumps(ack), retain = True)

    def sendmsg_to_mqtthub(self, send_msg):
        chat = "/cloud/wdtarm/test1/0/data"
        self.__mqtt__.publish(chat, payload = json.dumps(send_msg), retain = True)

    def run(self):
        self.__mqtt__.loop_forever()

class mqtt_run(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

        self.hardware_data = hw_data()

        # mqtt start thread
        self.mqtt_operation = mqtt_operation("mqtt_main_thread")
        self.mqtt_operation.start()

    def run(self):
        while True :
            self.hardware_data.get_hw_data()
            self.mqtt_operation.sendmsg_to_mqtthub(self.hardware_data.send_msg)
            #print("sendmsg to mqtt hub")
            time.sleep(config.config["sensor"]["timing"])
