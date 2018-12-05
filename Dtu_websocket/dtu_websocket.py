#!/usr/bin/python3

import threading
import time
import sys
import json
from websocket_server import WebsocketServer

sys.path.append("../")

from Config.config import *
from Dtu_dev.dtu_dev import *

class dtu_websocket(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.port = 9001
        self.addr = "0.0.0.0"

    def new_client(self, client, server):
        print("new clinet %d" % client["id"])

    def client_left(self, client, server):
        print(" clinet %d lift" % client["id"])

    def client_msg_received(self, client, server, message):
        print(message)

        self.temp_humi_cmd = [0x1, 0x3, 0x0, 0x0, 0x0, 0x2, 0xc4, 0xb]

        dtu_dev.network_recv_queue.put(self.temp_humi_cmd)

        time.sleep(0.5)
        self.server_send(client)

    def server_send(self, client):
        send_msg = {
                "type" : "uart_read",
                "unit" : "int",
                "temp_data" : -1,
                "humi_data" : -1,
                "uart_name" : "/dev/ttyO1",
                "uart_how_to_read" : "man"
                }

        try :
            msg = dtu_dev.network_send_queue.get(\
                timeout = dtu_config.config_data["network"]["timeout"])
        except :
            msg = None

        print(msg)

        if (len(msg) > 8):
            send_msg["temp_data"] = ((msg[3] << 8) + msg[4]) / 10
            send_msg["humi_data"] = ((msg[5] << 8) + msg[6]) / 10

        self.websocket_server.send_message(client, json.dumps(send_msg))

    def websocket_init(self):
        self.websocket_server = WebsocketServer(self.port, self.addr)
        self.websocket_server.set_fn_new_client(self.new_client)
        self.websocket_server.set_fn_client_left(self.client_left)
        self.websocket_server.set_fn_message_received(self.client_msg_received)
        self.websocket_server.run_forever()

    def run(self):
        self.websocket_init()
