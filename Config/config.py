#!/usr/bin/python3

import configparser
import os
import json
import time
import serial

class configure():

    __configure_file_path = "Config/config.json";

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, "_inst"):

            cls._inst = super(configure, cls).__new__(cls);

            try :
                cls.config_file = open(cls.__configure_file_path)
            except :
                cls.__configure_file_path = "../Config/config.json"
                cls.config_file = open(cls.__configure_file_path)
                #print("use other file path");

            cls.config = json.load(cls.config_file);

            cls.serial_cfg = cls.config["COM1"];

            cls.serial = serial.Serial(cls.serial_cfg['port'], cls.serial_cfg['baudrate'], timeout = cls.serial_cfg['timeout'])
            #cls.serial = serial.Serial(cls.serial_cfg['port'], cls.serial_cfg['baudrate'])
            cls.config_file.close()

        return cls._inst;

    def print_cfg(cls):
        pass;
        print(cls.config);

    def set_file_path(cls, filepath):
        cls.__configure_file_path = filepath;
        config = configure();

config = configure();

if __name__ == '__main__':
    config.set_file_path("Config/config.json");
    config.print_cfg();

