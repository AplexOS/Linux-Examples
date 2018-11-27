#!/usr/bin/python3

import socket
import sys
import threading
import time

sys.path.append("../")

from Config.config import *
from Dtu_dev.dtu_dev import *

class dtu_server(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        self.client_socket, self.addr = dtu_dev.socket.accept()

        dtu_dev.socket.setblocking(True)
        dtu_dev.socket.settimeout(5)

        print(self.addr)
        print("new clinet start")

        self.dtu_server_recv = dtu_server_run("server_recv", self.client_socket, 1)
        self.dtu_server_send = dtu_server_run("server_send", self.client_socket, 0)

        self.dtu_server_recv.start()
        self.dtu_server_send.start()

        self.dtu_server_recv.join()

class dtu_server_run(threading.Thread):
    def __init__(self, name, client_socket, flag):
        threading.Thread.__init__(self)
        self.name = name
        self.client_socket = client_socket
        self.flag = flag

    def socket_recv(self):
        while True :
            try :
                msg = self.client_socket.recv(1024)
                print(msg)
                print("test socket recv msg")
            except :
                print("recv socket data error or timeout")
            else :
                if (not dtu_dev.network_recv_queue.full()) :
                    dtu_dev.network_recv_queue.put(msg)

    def socket_send(self):
        while True :
            try :
                msg = dtu_dev.network_send_queue.get(timeout=5)
                self.client_socket.send(msg)
                print("test socket send msg")
            except :
                print("socket send msg fail or queue timeout")

    def run(self):
        while True :
            if (self.flag == 1) :
                self.socket_recv()
            elif (self.flag == 0):
                self.socket_send()

class dtu_client(threading.Thread):
    def __init__(self, name, flag):
        threading.Thread.__init__(self)
        self.name = name
        self.flag = flag

    def run(self):
        while True :
            if (self.flag == 1) and (not dtu_dev.network_recv_queue.full()):
                dtu_dev.network_recv_queue.put(dtu_dev.socket.recv(1024))
                time.sleep(3)
                print("eth write mas to queue")
            elif (self.flag == 0) and (not dtu_dev.network_send_queue.empty()) :
                dtu_dev.socket.send(dtu_dev.network_send_queue.get())
                time.sleep(3)
                print("eth write msg to socketk")
            else :
                time.sleep(3)

        dtu_dev.socket.close()

class dtu_network(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        if dtu_config.config_data["network"]["type"] == "server" :
            dtu_network_server_send_msg = dtu_server("dtu_network_send")

            dtu_network_server_send_msg.start()

            dtu_network_server_send_msg.join()

        elif dtu_config.config_data["network"]["type"] == "client" :
            dtu_network_client_send_msg = dtu_client("dtu_network_send", 0)
            dtu_network_client_recv_msg = dtu_client("dtu_network_recv", 1)

            dtu_network_client_send_msg.start()
            dtu_network_client_recv_msg.start()

            dtu_network_client_recv_msg.join()

