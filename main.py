#!/usr/bin/python3

from Config.config import *
from Slave_dev.slave_dev import *
from Hw_operation.dev_operation import *
from Mqtt_operation.mqtt_operation import *

if __name__ == "__main__" :

    '''
    temp_dev = Temp_humi_dev()
    temp_slave_operation = dev_operation("temp_dev", config, temp_dev)
    temp_slave_operation.operation(0x1)

    illumination_dev = Illumination_detect()
    illumination_slave_operation = dev_operation("light_dev", config, Illumination_dev)
    illumination_slave_operation.operation(0x1)

    co2_dev = Co2_detect()
    co2_slave_operation = dev_operation("co2_dev", config, co2_dev)
    co2_slave_operation.operation(0x1)

    soil_dev = Soil_moisture_detect()
    soil_slave_operation = dev_operation("soil_dev", config, soil_dev)
    soil_slave_operation.operation(0x1)

    pressure_dev = Pressure_detect()
    pressure_slave_operation = dev_operation("case_dev", config, pressure_dev)
    pressure_slave_operation.operation(0x1)

    #slave_operation.set_dev_addr(0x5)
    '''

    mqtt_thread = mqtt_run("mqtt_thread")
    mqtt_thread.start()
    mqtt_thread.join()

