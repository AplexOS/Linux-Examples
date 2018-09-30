#!/usr/bin/python3

import threading
import time
import signal
import os
import fcntl

class rainfull():
    def __init__(self):
        self.rain_data = 0

        self.gpio0_irq_file = open("/dev/switch")
        signal.signal(signal.SIGIO, self.get_rain_data)
        fcntl.fcntl(self.gpio0_irq_file, fcntl.F_SETOWN, os.getpid())
        flags = fcntl.fcntl(self.gpio0_irq_file, fcntl.F_GETFL);
        flags |= os.O_ASYNC;
        fcntl.fcntl(self.gpio0_irq_file, fcntl.F_SETFL, flags);

        self.time_before = time.time()
        self.time_after = 0

    def get_rain_data(self, signum, frame):
        self.time_after = time.time()

        if((self.time_after - self.time_before) > 5) :
            self.rain_data += 1
            #print(self.rain_data)

        self.time_before  = self.time_after

