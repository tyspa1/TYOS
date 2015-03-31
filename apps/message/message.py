#Call App
#copyright (c) 2015 Tyler Spadgenske
#MIT License
###############################
#To be packaged with stock TYOS
###############################

import pygame
from pygame.locals import *

class Run():
    def __init__(self, fona):
        #Load images
        self.keyboard_image = pygame.image.load('/home/pi/tyos/apps/message/keyboard.png')
        self.keyboard_rect = self.keyboard_image.get_rect()
        self.keyboard_rect.x = 6
        self.keyboard_rect.y = 290
        
        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit = {'surfaces':[self.keyboard_image], 'rects':[self.keyboard_rect]}

    def run_app(self):
        pass

    def get_events(self, event):
        #Get key pressed
        #Row 1
        if event.pos[1] > 290 and event.pos[1] < 330:
            print 'Row 1'
            if event.pos[0] > 6 and event.pos[0] < 31:
                print 'q'
            if event.pos[0] > 37 and event.pos[0] < 62:
                print 'w'
            if event.pos[0] > 68 and event.pos[0] < 93:
                print 'e'
            if event.pos[0] > 99 and event.pos[0] < 124:
                print 'r'
            if event.pos[0] > 130 and event.pos[0] < 155:
                print 't'
            if event.pos[0] > 161 and event.pos[0] < 186:
                print 'y'
            if event.pos[0] > 192 and event.pos[0] < 217:
                print 'u'
            if event.pos[0] > 223 and event.pos[0] < 248:
                print 'i'
            if event.pos[0] > 254 and event.pos[0] < 279:
                print 'o'
            if event.pos[0] > 285 and event.pos[0] < 310:
                print 'p'
                
        if event.pos[1] > 336 and event.pos[1] < 376:
            print 'Row 2'
        if event.pos[1] > 382 and event.pos[1] < 422:
            print 'Row 3'
        if event.pos[1] > 428 and event.pos[1] < 468:
            print 'Row 4'
            
