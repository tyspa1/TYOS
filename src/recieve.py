#Recieve calls and sms messages
#copyright 2015 (c) Tyler Spadgenske

import time, pygame
import RPi.GPIO as io

class Recieve():
    def __init__(self, fona):
        io.setmode(io.BCM)
        io.setup(4, io.IN)
        
        self.fona = fona
        self.mode = 0
        self.pressed = False
        self.call_coming = False

        #Colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        
        #Setup images
        self.call_image = pygame.image.load('/home/pi/tyos/apps/call/call.png')
        self.hangup_image = pygame.image.load('/home/pi/tyos/apps/call/hangup.png')

        #Setup rects
        self.call_rect = self.call_image.get_rect()
        self.call_rect.y = 390
        self.call_rect.x = 125

        #Setup fonts
        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 24)

        #Setup numbers Text
        self.incoming = self.font.render('Incoming Call...', True, self.BLACK, self.WHITE)
        self.incoming_rect = self.incoming.get_rect()
        self.incoming_rect.centerx = 160
        self.incoming_rect.centery = 330

        self.blit = {'surfaces':[self.call_image, self.incoming], 'rects':[self.call_rect, self.incoming_rect]}

    def check(self, update):
        if io.input(4) == 0:
            self.call_coming = True
            update = True
        if self.call_coming:
            self.incoming_call()
        return update

    def incoming_call(self):
        if self.pressed:
            self.mode += 1
            self.pressed = False
            
            if self.mode == 1:
                print 'picking up...'
                self.fona.transmit('ATA')
                self.blit['surfaces'][0] = self.hangup_image
            if self.mode == 2:
                print 'hanging up'
                self.fona.transmit('ATH')
                self.blit['surfaces'][0] = self.call_image
                self.call_coming = False
                self.mode = 0

    def get_events(self, event):
        if event.type == pygame.locals.MOUSEBUTTONUP:
            if event.pos[0] > 140 and event.pos[0] < 210:
                if event.pos[1] > 390 and event.pos[1] < 460:
                    self.pressed = True
