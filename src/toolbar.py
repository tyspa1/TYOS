#App Toolbar
#copyright (c) 2015 Tyler Spadgenske
#GPL License

import serialport, time
import pygame
from pygame.locals import *

class Toolbar():
    def __init__(self):
        self.UPDATE_TIME = 10
        #Setup fona
        self.fona = serialport.SerialPort()
        self.fona.connect()

        #Define colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

        #Setup fonts
        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 14)
        
        #Setup Battery Persentage Text
        self.bat_left = self.font.render('..%', True, self.BLACK, self.WHITE)
        self.bat_left_rect = self.bat_left.get_rect()
        self.bat_left_rect.centerx = 285
        self.bat_left_rect.centery = 15

        #Setup clock
        self.last_update = time.time()

    def check_reception(self, rects):
        self.raw_reception = self.fona.transmit('AT+CSQ')
        self.raw_reception = self.raw_reception[1]

        #Remove line feeds and echo
        for i in self.raw_reception:
            if i != ' ':
                self.raw_reception = self.raw_reception.replace(i, '', 1)
            else:
                self.raw_reception = self.raw_reception.replace(i, '', 1)
                break
            
        #Extract dbm
        for i in reversed(self.raw_reception):
            if i != ',':
                self.raw_reception = self.raw_reception.replace(i, '', 1)
            else:
                self.raw_reception = self.raw_reception.replace(i, '', 1)
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

        print 'BARS:' + str(self.bars)
        
        #Reception Bar rects      x   y  w  h
        self.one =   pygame.Rect(10, 18, 5, 7)
        self.two =   pygame.Rect(23, 13, 5, 12)
        self.three = pygame.Rect(38,  8, 5, 17)
        self.four =  pygame.Rect(53,  3, 5, 22)

        self.WHITE = (255,255,255)

        rects = {'rects':[], 'colors':[]}
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
    
    def check_battery(self, text):

        #Get battery level from fona
        self.raw_data = self.fona.transmit('AT+CBC')
        self.raw_data = self.raw_data[1]

        #Remove line feeds and echo
        for i in self.raw_data:
            if i != ',':
                self.raw_data = self.raw_data.replace(i, '', 1)
            else:
                break
        
        #Extract percentage
        for i in reversed(self.raw_data):
            if i != ',':
                self.raw_data = self.raw_data.replace(i, '', 1)
            else:
                break

        #Put percentage in text
        self.percentage = self.raw_data.replace(',', '')   

        print 'BATTERY LEVEL: ' + self.percentage + '%'

        text['surface'] = self.font.render(self.percentage + '%', True, self.BLACK, self.WHITE)
        
        return text

    def clock(self, rects, text, update):
        if time.time() - self.last_update > self.UPDATE_TIME:
            print 'UPDATING...'
            self.last_update = time.time()
            
            rects = self.check_reception(rects)
            text = self.check_battery(text)
            update = True

        return rects, text, update

if __name__ == '__main__':
    pygame.init()
    t = Toolbar()
    t.clock()
