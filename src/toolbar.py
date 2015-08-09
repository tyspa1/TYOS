#App Toolbar
#copyright (c) 2015 Tyler Spadgenske
#MIT License

import time
import os
import pygame
from pygame.locals import *

class Toolbar():
    def __init__(self, fona):
        self.UPDATE_TIME = 30
        self.DEAD = 30
        
        #Setup fona
        self.fona = fona

        #Define colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

        self.dead_bat = False

        #Setup fonts
        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 14)
        
        #Setup Battery Persentage Text
        self.bat_left = self.font.render('..%', True, self.BLACK, self.WHITE)
        self.bat_left_rect = self.bat_left.get_rect()
        self.bat_left_rect.centerx = 285
        self.bat_left_rect.centery = 15

        #Set the Pi clock to the Fona RTC
        self.rtc()

        #Setup reception/battery clock
        self.last_update = time.time()
        
    def rtc(self):
        #Get time from RTC on FONA
        self.rtc_time = self.fona.transmit('AT+CCLK?')
        self.rtc_time = self.rtc_time[1]

        #Parse string to include hours and seconds only
        self.rtc_time = self.rtc_time.split(',') 
        self.rtc_time = self.rtc_time[1]
        self.rtc_time = self.rtc_time.split('-')
        self.rtc_time = self.rtc_time[0]

        print self.rtc_time

        print 'RTC TIME:'

        #Set Overall Time
        os.system('sudo date +%T -s "' + self.rtc_time + '"')

    def check_reception(self, rects, y):
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
        try: 
            self.reception = int(self.raw_reception)
        except:
            self.reception = 0
            print 'ERROR'

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
        self.one =   pygame.Rect(10, y + 18, 5, 7)
        self.two =   pygame.Rect(23, y + 13, 5, 12)
        self.three = pygame.Rect(38,  y + 8, 5, 17)
        self.four =  pygame.Rect(53,  y + 3, 5, 22)

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

        print 'RECEPTION: ' + str(self.reception) + 'dbm'

        return rects
    
    def check_battery(self, text):

        #Get battery level from fona
        self.raw_data = self.fona.transmit('AT+CBC')
        self.raw_data = self.raw_data[1]
        self.raw_data = self.raw_data.split(',')
        self.percentage = self.raw_data[1]

        print 'BATTERY LEVEL: ' + self.percentage + '%'
        if int(self.percentage) < self.DEAD:
            self.dead_bat = True

        text['surface'] = self.font.render(self.percentage + '%', True, self.BLACK, self.WHITE)
        
        return text

    def clock(self, rects, text, update, y):
        if time.time() - self.last_update > self.UPDATE_TIME:
            print 'UPDATING...'
            self.last_update = time.time()
            
            rects = self.check_reception(rects, y)
            text = self.check_battery(text)
            update = True

        return rects, text, update, self.dead_bat

if __name__ == '__main__':
    pygame.init()
    t = Toolbar()
    t.blit_time()
