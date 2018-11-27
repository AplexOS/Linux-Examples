#!/usr/bin/python3

from Dtu_eth.dtu_eth import *
from Dtu_serial.dtu_serial import *
from Config.config import *
from Dtu_dev.dtu_dev import *

if __name__ == "__main__" :
    serial_read_pre = dtu_serial("serial_read", dtu_dev.serial_com1, 0)
    serial_write_pre = dtu_serial("serial_write", dtu_dev.serial_com1, 1)
    network_pre = dtu_network("network_pro")

    serial_read_pre.start()
    serial_write_pre.start()
    network_pre.start()

    serial_read_pre.join()
