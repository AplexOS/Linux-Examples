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

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

class aplex_mqtt(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.config = config_data.config
        self.__mutex = threading.Semaphore()

        self.init_connect()

    def init_connect(self):
        self.__mutex.acquire()

        self.__mqtt_id = str(math.floor(time.time()))
        self.__mqtt__ = mqtt.Client(self.__mqtt_id)
        self.__mqtt__.username_pw_set(self.config["mqtt"]["username"], \
                self.config["mqtt"]["passwd"])
        self.__mqtt__.on_connect = self.on_connect
        self.__mqtt__.on_disconnect = self.on_disconnect
        self.__mqtt__.on_message = self.recvmsg_from_mqtthub

        self.__mutex.release()

        self.try_connect_to_mqtthub()

    def on_connect(self, client, userdata, flags, rc):
        try :
            client.subscribe("v1/gateway/rpc")
            client.subscribe("v1/gateway/attributes")
            client.subscribe("v1/gateway/attributes/response")
        except :
            print("sub eroor")
        else :
            print("sub ok")

        self.device_connect("1001")
        self.device_connect("1101")
        self.device_connect("1201")
        self.device_connect("1301")

        self.pub_sensor_atrribute()

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logging.debug("disconect start")
            self.try_connect_to_mqtthub()
            logging.debug("disconect stop")
            time.sleep(2)

    def try_connect_to_mqtthub(self):
        while True :
            try :
                logging.debug("connect start")
                self.__mqtt__.connect(self.config["mqtt"]["wss_addr"], \
                        self.config["mqtt"]["wss_port"], keepalive=10)
            except :
                logging.debug("connect error")
                time.sleep(2)
            else :
                logging.debug("connect success")
                break

    def recvmsg_from_mqtthub(self, client, userdata, msg):
        try :
            json_data = json.loads(msg.payload.decode('utf8'))
            logging.debug(json_data)
        except :
            logging.debug("decode msg error")
        else:
            pass

    def device_connect(self, device_id):
        topic = "v1/gateway/connect"
        message = {
                "message" : {
                    "device" : "1001"
                    }
                }
        message["message"]["device"] = device_id
        try :
            self.__mqtt__.publish(topic, payload = json.dumps(message), retain = False)
        except :
            print("publish error")

    def device_disconnect(self, device_id):
        topic = "v1/gateway/disconnect"
        message = {
                "message" : {
                    "device" : "1001"
                    }
                }
        message["message"]["device"] = device_id
        try :
            self.__mqtt__.publish(topic, payload = json.dumps(message), retain = False)
        except :
            print("publish error")

    def publish_data(self):
        topic = "v1/gateway/attributes"
        message = {
                "Message": {
                    "1001":{
                        "attribute1":"value1",
                        "attribute2": 42
                        },
                    "1201":{
                        "attribute1":"value1",
                        "attribute2": 42
                        }
                    }
                }
        try :
            self.__mqtt__.publish(topic, payload = json.dumps(message), retain = False)
        except :
            print("publish error")

    def find_atrribute1(self):
        topic = "v1/gateway/attributes/request"
        message = {
                "Message": {
                    "id": "1",
                    "device": "5100100001001201904020003",
                    "client": True,
                    "key": "attribute1"
                    }
                }
        try :
            self.__mqtt__.publish(topic, payload = json.dumps(message), retain = False)
        except :
            print("publish error")

    def sub_shared_attribute(self):
        topic =  "v1/gateway/attributes"
        message = {
                "Message" : {
                    "device": "5100100001001201904020003",
                    "data": {
                        "attribute1": "value1",
                        "attribute2": 42
                        }
                    }
                }

    def pub_sensor_atrribute(self):
        topic = "v1/gateway/telemetry"
        message = {
                "Message" :{
                    "1001": [
                        {
                            "ts": 1483228800000,
                            "values": {
                                "temperature": 23
                                }
                            }
                        ],
                    "1101": [
                        {
                            "ts": 1483228800000,
                            "values": {
                                "humidity": 56
                                }
                            }
                        ],
                    "1201": [
                        {
                            "ts": 1483228800000,
                            "values": {
                                "light_intensity": 2300
                                }
                            }
                        ],
                    "1301": [
                        {
                            "ts": 1483228800000,
                            "values": {
                                "CO2_concentration": 450
                                }
                            }
                        ]
                    }
                }

        while True :
            time.sleep(5)
            try :
                self.__mqtt__.publish(topic, payload = json.dumps(message), retain = False)
            except :
                print("publish error")

    def run(self):
        self.__mqtt__.loop_forever()

if __name__ == "__main__":
    test = aplex_mqtt()
    test.start()
    test.join()
