#!/usr/bin/python3

import configparser
import os
import json
import time

class configure():

    __configure_file_path = "Config/config.json";
    __configure_device_file_path = "Config/config_device.json";

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, "_inst"):

            cls._inst = super(configure, cls).__new__(cls);

            try :
                cls.config_file = open(cls.__configure_file_path)
                cls.config_device_file = open(cls.__configure_device_file_path)
            except :
                cls.__configure_file_path = "../Config/config.json"
                cls.config_file = open(cls.__configure_file_path)

                cls.__configure_device_file_path = "../Config/config_device.json"
                cls.config_device_file = open(cls.__configure_device_file_path)

            cls.config = json.load(cls.config_file);
            cls.config_device = json.load(cls.config_device_file);

            cls.e_longitude = -1
            cls.n_latitude = -1

            cls.config_file.close()
            cls.config_device_file.close()

            serial_id = "-1"
            eeprom_fd = open("/dev/eeprom", "rb")
            try :
                serial_id = eeprom_fd.read(25).decode()
            except :
                serial_id = "-1"

            eeprom_fd.close()

            cls.config["device"]["id"] = serial_id

        return cls._inst;

    def print_cfg(cls):
        print(cls.config);
        print(cls.config_device);

    def set_file_path(cls, filepath1, filepath2):
        cls.__configure_file_path = filepath1;
        cls.__configure_device_file_path = filepath2;

    def save_config_data(cls):
        try :
            with open(cls.__configure_file_path, "w") as config_file :
                config_file.write(json.dumps(cls.config))
            os.system("sync")
        except :
            print("write config data error")

        os.system("sync")

    def save_config_device_data(cls):
        try :
            with open(cls.__configure_device_file_path, "w") as config_device_file :
                config_device_file.write(json.dumps(cls.config_device))
            os.system("sync")
        except :
            print("write config data error")

        os.system("sync")

config = configure();

if __name__ == '__main__':
    config.set_file_path("Config/config.json", "Config/config_device.json");
    config.print_cfg();

