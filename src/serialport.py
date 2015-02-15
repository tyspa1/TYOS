# -*- coding: utf-8 -*-
#TYOS Serial Interface with Fona and RTC
#copyright (c) 2015 Tyler Spadgenske

import serial, time

class SerialPort():
    def __init__(self):
       pass
    
    def connect(self):
        #open connection
        self.serialport = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
        #Send test command
        self.serialport.write('\nAT')
        #get reply 
        reply = self.serialport.readlines()
        print(reply)
        #Check for good return
        try:
            if reply[1][0] == 'O':
                print 'Ćonnected to FONA'
            else:
                print 'Error Comunicating with FONA'
        except:
            print 'Error comunicating with FONA'
    def transmit(self, data):
        self.serialport.write('\n' + data)
        self.serialport.readlines()
        print self.serialport.readlines()
    
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
