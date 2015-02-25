# -*- coding: utf-8 -*-
#TYOS Serial Interface with Fona and RTC
#copyright (c) 2015 Tyler Spadgenske

import serial, time

class SerialPort():
    def __init__(self):
       self.baud_rate = 115200
       
    def connect(self):
        #open connection
        self.serialport = serial.Serial("/dev/ttyAMA0", self.baud_rate, timeout=0.5)
        #Send test command
        self.serialport.write('AT\r')
        #get reply 
        reply = self.serialport.read(50).rstrip()
        print(reply)
        #Check for good return
        if 'OK' in reply:
            print 'Connected to FONA'
        else:
            print 'Error Comunicating with FONA'
            self.serialport.close()

    def transmit(self, data):
        self.serialport.write(data + '\r')
        feed = self.serialport.readlines()
        for i in range(len(feed)):
            feed[i] = feed[i].rstrip()
        return feed
    
    def check(self):
        self.model = self.transmit('ATI')
        print self.model
        
    def battery(self):
        pass

    def sms(self):
        pass

    def call(self):
        pass
    
if __name__ == '__main__':
    test = SerialPort()
    test.connect()
    test.check()

