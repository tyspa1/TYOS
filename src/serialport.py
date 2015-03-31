# -*- coding: utf-8 -*-
#TYOS Serial Interface with Fona
#copyright (c) 2015 Tyler Spadgenske

import serial, time

class SerialPort():
    def __init__(self):
       self.baud_rate = 9600

    def connect(self):
        #open connection
        self.serialport = serial.Serial("/dev/ttyAMA0", self.baud_rate, timeout=0.5)
        #Send test command
        self.serialport.write('AT\r')
        #get reply 
        reply = self.serialport.readlines()
        for i in range(len(reply)):
            reply[i] = reply[i].rstrip()

        #Check for good return
        if 'OK' in reply:
            print 'Connected to FONA'
        else:
            print 'Error Comunicating with FONA'

    def transmit(self, data):
        self.serialport.write(data + '\r')
        feed = self.serialport.readlines()
        for i in range(len(feed)):
            feed[i] = feed[i].rstrip()
        return feed
    
    def check(self):
        self.model = self.transmit('ATI')
        print self.model

    def close(self):
        self.serialport.close()
        
if __name__ == '__main__':
    test = SerialPort()
    test.connect()
