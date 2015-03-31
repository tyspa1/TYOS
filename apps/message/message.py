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
        #Variables
        self.mode = 0 #0=number, 1=text
        self.number = ''
        self.message = ''
        
        #Load images
        self.keyboard_image = pygame.image.load('/home/pi/tyos/apps/message/keyboard.png')
        self.num_keyboard_image = pygame.image.load('/home/pi/tyos/apps/message/numbered_keyboard.png')
        self.bubble = pygame.image.load('/home/pi/tyos/apps/message/bubble.png')
        self.keyboard_rect = self.keyboard_image.get_rect()
        self.keyboard_rect.x = 6
        self.keyboard_rect.y = 290

        self.bubble_rect = self.bubble.get_rect()
        self.bubble_rect.x = 5
        self.bubble_rect.y = 50
        
        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit = {'surfaces':[self.keyboard_image, self.bubble], 'rects':[self.keyboard_rect, self.bubble_rect]}

    def run_app(self):
        pass

    def get_events(self, event):
        #Get key pressed
        #Row 1
        if event.pos[1] > 290 and event.pos[1] < 330:
            if event.pos[0] > 6 and event.pos[0] < 31:
                print 'q'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 37 and event.pos[0] < 62:
                print 'w'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 68 and event.pos[0] < 93:
                print 'e'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 99 and event.pos[0] < 124:
                print 'r'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 130 and event.pos[0] < 155:
                print 't'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 161 and event.pos[0] < 186:
                print 'y'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 192 and event.pos[0] < 217:
                print 'u'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 223 and event.pos[0] < 248:
                print 'i'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 254 and event.pos[0] < 279:
                print 'o'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 285 and event.pos[0] < 310:
                print 'p'
                if self.mode == 1:
                    self.message.append('q')
        #Row 2  
        if event.pos[1] > 336 and event.pos[1] < 376:
            if event.pos[0] > 18 and event.pos[0] < 43:
                print 'a'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 49 and event.pos[0] < 74:
                print 's'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 80 and event.pos[0] < 115:
                print 'd'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 111 and event.pos[0] < 136:
                print 'f'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 142 and event.pos[0] < 167:
                print 'g'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 173 and event.pos[0] < 198:
                print 'h'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 204 and event.pos[0] < 229:
                print 'j'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 235 and event.pos[0] < 260:
                print 'k'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 266 and event.pos[0] < 291:
                print 'l'
                if self.mode == 1:
                    self.message.append('q')
        #Row 3
        if event.pos[1] > 382 and event.pos[1] < 422:
            if event.pos[0] > 49 and event.pos[0] < 74:
                print 'z'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 80 and event.pos[0] < 115:
                print 'x'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 111 and event.pos[0] < 136:
                print 'c'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 142 and event.pos[0] < 167:
                print 'v'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 173 and event.pos[0] < 198:
                print 'b'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 204 and event.pos[0] < 229:
                print 'n'
                if self.mode == 1:
                    self.message.append('q')
            if event.pos[0] > 235 and event.pos[0] < 260:
                print 'm'
                if self.mode == 1:
                    self.message.append('q')
        #Row 4
        if event.pos[1] > 428 and event.pos[1] < 468:
            if event.pos[0] > 49 and event.pos[0] < 115:
                print 'back'
            if event.pos[0] > 111 and event.pos[0] < 198:
                print 'space'
            if event.pos[0] > 204 and event.pos[0] < 260:
                print 'send'

        #Keyboard mode
        if event.pos[0] > 5 and event.pos[0] < 318 and event.pos[1] > 50 and event.pos[1] < 78:
            print 'number mode'
            self.mode = 0
        if event.pos[0] > 5 and event.pos[0] < 318 and event.pos[1] > 88 and event.pos[1] < 218:
            print 'message mode'
            self.mode = 1
            
        if self.mode == 0:
            self.blit['surfaces'][0] = self.num_keyboard_image
        else:
            self.blit['surfaces'][0] = self.keyboard_image
            
