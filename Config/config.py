#!/usr/bin/python3

import configparser
import os
import json
import time

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

                cls.__configure_device_file_path = "../Config/config_device.json"

            cls.config = json.load(cls.config_file);

            cls.config_file.close()

            serial_id = "-1"
            try :
                eeprom_fd = open("/dev/eeprom", "rb")
                serial_id = eeprom_fd.read(25).decode()
            except :
                serial_id = "-1"
            else :
                eeprom_fd.close()

            cls.config["device"]["id"] = serial_id

        return cls._inst;

    def print_cfg(cls):
        print(cls.config);

    def set_file_path(cls, filepath1):
        cls.__configure_file_path = filepath1;

    def save_config_data(cls):
        os.system("sync")
        try :
            with open(cls.__configure_file_path, "w") as config_file :
                config_file.write(json.dumps(cls.config))
            os.system("sync")
        except :
            print("write config data error")

        os.system("sync")

config_data = configure();

if __name__ == '__main__':
    config.set_file_path("Config/config.json");
    config.print_cfg();

