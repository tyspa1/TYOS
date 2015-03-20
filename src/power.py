#Startup/shutdown script
#copyright 2015 (c) Tyler Spadgenske

import RPi.GPIO as io
import time

class Power():
    def __init__(self):
        self.PWR = 21
        io.setwarnings(False)
        io.setmode(io.BCM)
        io.setup(self.PWR, io.OUT)

    def toggle(self):
        io.output(self.PWR, 1)
        time.sleep(2.5)
        io.output(self.PWR, 0)

test = Power()
test.toggle()
