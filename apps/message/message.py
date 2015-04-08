#Message App
#copyright (c) 2015 Tyler Spadgenske
#MIT License
###############################
#To be packaged with stock TYOS
###############################

import pygame, time
from pygame.locals import *

class Run():
    def __init__(self, fona):
        self.fona = fona
        
        #Colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.send = False
        self.valid = False
        
        #Variables
        self.mode = 2
        self.number = ''
        self.message = ''
        
        #Load images
        self.keyboard_image = pygame.image.load('/home/pi/tyos/apps/message/keyboard.png')
        self.num_keyboard_image = pygame.image.load('/home/pi/tyos/apps/message/numbered_keyboard.png')
        self.bubble = pygame.image.load('/home/pi/tyos/apps/message/bubble.png')
        self.keyboard_rect = self.keyboard_image.get_rect()
        self.keyboard_rect.x = 6
        self.keyboard_rect.y = 293

        #Main conversation image
        self.conversation_image = pygame.image.load('/home/pi/tyos/apps/message/conversation.png')
        self.conversation_rect = self.conversation_image.get_rect()
        self.conversation_rect.centerx = 160
        self.conversation_rect.centery = 260
        
        #Setup text
        #Setup fonts
        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 20)
        self.message_font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 12)
        
        #Says... text
        self.says_text1 = self.font.render('Tyler says...', True, self.BLACK, self.WHITE)
        self.says_rect1 = self.says_text1.get_rect()
        self.says_rect1.x = 35
        self.says_rect1.y = 120
        self.says_text2 = self.font.render('Billy says...', True, self.BLACK, self.WHITE)
        self.says_rect2 = self.says_text2.get_rect()
        self.says_rect2.x = 35
        self.says_rect2.y = 233

        #Message lines
        self.message_line1 = self.font.render('aaaaa', True, self.BLACK, self.WHITE)
        self.message_line1_rect = self.message_line1.get_rect()
        self.message_line1_rect.x = 42
        self.message_line1_rect.y = 155
        self.message_line2 = self.font.render('bbbbb', True, self.BLACK, self.WHITE)
        self.message_line2_rect = self.message_line2.get_rect()
        self.message_line2_rect.x = 42
        self.message_line2_rect.y = 175
        self.message_line3 = self.font.render('ccccccc', True, self.BLACK, self.WHITE)
        self.message_line3_rect = self.message_line3.get_rect()
        self.message_line3_rect.x = 42
        self.message_line3_rect.y = 195
        
        #Number to send
        #Setup numbers Text
        self.number_text = self.font.render(self.number, True, self.BLACK, self.WHITE)
        self.number_rect = self.number_text.get_rect()
        self.number_rect.x = 15
        self.number_rect.y = 57
        
        #Setup numbers Text
        self.line1 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line1_rect = self.line1.get_rect()
        self.line1_rect.x = 15
        self.line1_rect.y = 130

        #Setup numbers Text
        self.line2 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line2_rect = self.line2.get_rect()
        self.line2_rect.x = 15
        self.line2_rect.y = 150

        #Setup numbers Text
        self.line3 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line3_rect = self.line3.get_rect()
        self.line3_rect.x = 15
        self.line3_rect.y = 170
        
        self.bubble_rect = self.bubble.get_rect()
        self.bubble_rect.x = 5
        self.bubble_rect.y = 50
        
        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit_mode1 = {'surfaces':[self.keyboard_image, self.bubble, self.line1, self.line2,
                                 self.line3, self.number_text], 'rects':[self.keyboard_rect, self.bubble_rect, self.line1_rect, self.line2_rect,
                                                       self.line3_rect, self.number_rect]}
        self.blit_mode2 = {'surfaces':[self.conversation_image, self.says_text1, self.says_text2, self.message_line1, self.message_line2, self.message_line3], 'rects':[self.conversation_rect,
                                                                                           self.says_rect1, self.says_rect2, self.message_line1_rect, self.message_line2_rect, self.message_line3_rect]}
        self.blit = self.blit_mode2
        
    def run_app(self):
        if len(self.number) == 10:
            self.valid = True
        else:
            self.valid = False
            self.send = False
        if self.send and self.valid:
            self.send = False
            self.valid = False
            self.fona.transmit('AT+CMGF=1')
            time.sleep(.25)
            self.fona.transmit('AT+CMGS="' + self.number + '"')
            time.sleep(0.25)
            self.fona.transmit(self.message)
            time.sleep(.25)
            self.fona.transmit(chr(26))
            self.mode = 2
            self.blit = self.blit_mode2

    def get_events(self, event):
        if self.mode != 2:
            self.get_keyboard_events(event)
        else:
            self.get_read_events(event)

    def get_read_events(self, event):
        if event.pos[0] > 35 and event.pos[0] < 285:
            if event.pos[1] > 62 and event.pos[1] < 105:
                print 'up arrow'
            if event.pos[1] > 352 and event.pos[1] < 403:
                print 'down arrow'
            if event.pos[1] > 410 and event.pos[1] < 455:
                self.mode = 0
                self.blit = self.blit_mode1
            
    def get_keyboard_events(self, event):
        #Get key pressed
        #Row 1
        if event.pos[1] > 290 and event.pos[1] < 330:
            if event.pos[0] > 6 and event.pos[0] < 31:
                if self.mode == 1:
                    self.message = self.message + 'q'
                else:
                    self.number = self.number + '1'
            if event.pos[0] > 37 and event.pos[0] < 62:
                if self.mode == 1:
                    self.message = self.message + 'w'
                else:
                    self.number = self.number + '2'
            if event.pos[0] > 68 and event.pos[0] < 93:
                if self.mode == 1:
                    self.message = self.message + 'e'
                else:
                    self.number = self.number + '3'
            if event.pos[0] > 99 and event.pos[0] < 124:
                if self.mode == 1:
                    self.message = self.message + 'r'
                else:
                    self.number = self.number + '4'
            if event.pos[0] > 130 and event.pos[0] < 155:
                if self.mode == 1:
                    self.message = self.message + 't'
                else:
                    self.number = self.number + '5'
            if event.pos[0] > 161 and event.pos[0] < 186:
                if self.mode == 1:
                    self.message = self.message + 'y'
                else:
                    self.number = self.number + '6'
            if event.pos[0] > 192 and event.pos[0] < 217:
                if self.mode == 1:
                    self.message = self.message + 'u'
                else:
                    self.number = self.number + '7'
            if event.pos[0] > 223 and event.pos[0] < 248:
                if self.mode == 1:
                    self.message = self.message + 'i'
                else:
                    self.number = self.number + '8'
            if event.pos[0] > 254 and event.pos[0] < 279:
                if self.mode == 1:
                    self.message = self.message + 'o'
                else:
                    self.number = self.number + '9'
            if event.pos[0] > 285 and event.pos[0] < 310:
                if self.mode == 1:
                    self.message = self.message + 'p'
                else:
                    self.number = self.number + '0'
        #Row 2  
        if event.pos[1] > 336 and event.pos[1] < 376:
            if event.pos[0] > 18 and event.pos[0] < 43:
                if self.mode == 1:
                    self.message = self.message + 'a'
            if event.pos[0] > 49 and event.pos[0] < 74:
                if self.mode == 1:
                    self.message = self.message + 's'
            if event.pos[0] > 80 and event.pos[0] < 115:
                if self.mode == 1:
                    self.message = self.message + 'd'
            if event.pos[0] > 111 and event.pos[0] < 136:
                if self.mode == 1:
                    self.message = self.message + 'f'
            if event.pos[0] > 142 and event.pos[0] < 167:
                if self.mode == 1:
                    self.message = self.message + 'g'
            if event.pos[0] > 173 and event.pos[0] < 198:
                if self.mode == 1:
                    self.message = self.message + 'h'
            if event.pos[0] > 204 and event.pos[0] < 229:
                if self.mode == 1:
                    self.message = self.message + 'j'
            if event.pos[0] > 235 and event.pos[0] < 260:
                if self.mode == 1:
                    self.message = self.message + 'k'
            if event.pos[0] > 266 and event.pos[0] < 291:
                if self.mode == 1:
                    self.message = self.message + 'l'
        #Row 3
        if event.pos[1] > 382 and event.pos[1] < 422:
            if event.pos[0] > 49 and event.pos[0] < 74:
                if self.mode == 1:
                    self.message = self.message + 'z'
            if event.pos[0] > 80 and event.pos[0] < 115:
                if self.mode == 1:
                    self.message = self.message + 'x'
            if event.pos[0] > 111 and event.pos[0] < 136:
                if self.mode == 1:
                    self.message = self.message + 'c'
            if event.pos[0] > 142 and event.pos[0] < 167:
                if self.mode == 1:
                    self.message = self.message + 'v'
            if event.pos[0] > 173 and event.pos[0] < 198:
                if self.mode == 1:
                    self.message = self.message + 'b'
            if event.pos[0] > 204 and event.pos[0] < 229:
                if self.mode == 1:
                    self.message = self.message + 'n'
            if event.pos[0] > 235 and event.pos[0] < 260:
                if self.mode == 1:
                    self.message = self.message + 'm'
        #Row 4
        if event.pos[1] > 428 and event.pos[1] < 468:
            if event.pos[0] > 49 and event.pos[0] < 115:
                if self.mode == 1:
                    self.message = self.message[:-1]
                else:
                    self.number = self.number[:-1]
            if event.pos[0] > 111 and event.pos[0] < 198:
                if self.mode == 1:
                    self.message = self.message + ' '
            if event.pos[0] > 204 and event.pos[0] < 260:
                self.send = True

        #Keyboard mode
        if event.pos[0] > 5 and event.pos[0] < 318 and event.pos[1] > 50 and event.pos[1] < 78:
            self.mode = 0
        if event.pos[0] > 5 and event.pos[0] < 318 and event.pos[1] > 88 and event.pos[1] < 218:
            self.mode = 1
            
        if self.mode == 0:
            self.blit['surfaces'][0] = self.num_keyboard_image
        else:
            self.blit['surfaces'][0] = self.keyboard_image

        self.blit['surfaces'][2] = self.font.render(self.message[:32], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][3] = self.font.render(self.message[32:64], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][4] = self.font.render(self.message[64:96], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][5] = self.font.render(self.number, True, self.BLACK, self.WHITE)
