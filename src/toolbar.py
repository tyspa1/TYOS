#App Toolbar
#copyright (c) 2015 Tyler Spadgenske
#GPL License

import serialport
import pygame
from pygame.locals import *

class Toolbar():
    def __init__(self):
        self.fona = serialport.SerialPort()
        self.fona.connect()

    def check_reception(self, rects):
        self.raw_reception = self.fona.transmit('AT+CSQ')
        self.raw_reception = self.raw_reception[1]

        #Remove line feeds and echo
        for i in self.raw_reception:
            if i != ' ':
                self.raw_reception = self.raw_reception.replace(i, '')
            else:
                self.raw_reception = self.raw_reception.replace(i, '')
                break
            
        #Extract dbm
        for i in reversed(self.raw_reception):
            if i != ',':
                self.raw_reception = self.raw_reception.replace(i, '')
            else:
                self.raw_reception = self.raw_reception.replace(i, '')
                break
            
        self.reception = int(self.raw_reception)

        #Convert to bars
        if self.reception > 23:
            self.bars = 4
        elif self.reception > 17:
            self.bars = 3
        elif self.reception > 12:
            self.bars = 2
        elif self.reception > 8:
            self.bars = 1
        else:
            self.bars = 0

        #Reception Bar rects      x   y  w  h
        self.one =   pygame.Rect(10, 18, 5, 7)
        self.two =   pygame.Rect(23, 13, 5, 12)
        self.three = pygame.Rect(38,  8, 5, 17)
        self.four =  pygame.Rect(53,  3, 5, 22)

        self.WHITE = (255,255,255)

        #Add them to list
        if self.bars > 3:
            rects['rects'].append(self.four)
            rects['colors'].append(self.WHITE)
        if self.bars > 2:
            rects['rects'].append(self.three)
            rects['colors'].append(self.WHITE)
        if self.bars > 1:
            rects['rects'].append(self.two)
            rects['colors'].append(self.WHITE)
        if self.bars > 0:
            rects['rects'].append(self.one)
            rects['colors'].append(self.WHITE)

        print 'RECEPTION: ' + str(self.reception)
        return rects
    
    def check_battery(self):
        pass

    def clock(self):
        pass

if __name__ == '__main__':
    t = Toolbar()
    t.check_reception()
