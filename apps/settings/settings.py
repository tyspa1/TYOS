#settings App
#copyright (c) 2015 Tyler Spadgenske
#MIT License
###############################
#To be packaged with stock TYOS
###############################

from subprocess import Popen
import sys
import pygame

class Run():
    def __init__(self, fona):
        self.fona = fona
        self.headset = False
        self.get_audio_mode()
        #Setup colors
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.WHITE = (255,255,255)
        
        self.menu = pygame.image.load('/home/pi/tyos/apps/settings/menu.png')
        self.menu_rect = self.menu.get_rect()

        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 32)

        self.off = self.font.render('OFF', True, self.RED, self.WHITE)
        # fona power Text
        self.fona_power = self.font.render('ON', True, self.GREEN, self.WHITE)
        self.fona_power_rect = self.off.get_rect()
        self.fona_power_rect.centerx = 280
        self.fona_power_rect.centery = 223
        self.on = self.font.render('ON', True, self.GREEN, self.WHITE)
        self.rect = self.off.get_rect()
        self.rect.centerx = 280
        self.rect.y = 158
        
        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit = {'surfaces':[self.menu, self.fona_power, self.off], 'rects':[self.menu_rect, self.fona_power_rect, self.rect]}

        #Set audio mode text
        if self.headset:
            self.blit['surfaces'][2] = self.on
        else:
            self.blit['surfaces'][2] = self.off
            
        self.next_app = None

    def get_audio_mode(self):
        audio_config = open('/home/pi/tyos/configure/audio.conf', 'r')
        file = audio_config.readlines()

        for i in range(0, len(file)):#Parse file
            if file[i][0] == '#':
                pass
                #Do Nothing. Line is comment
            else:
                file[i] = file[i].rstrip()
                if 'mode' in file[i]: #Extract audio mode: 1=Built in, 0=External
                    mode = file[i]
        
        mode = mode.split('=')
        self.mode = int(mode[1])

        if self.mode == 1:
            self.headset = False
        else:
            self.headset = True
        

    def run_app(self):
        pass
        
    def get_events(self, event):
        if event.pos[1] > 95 and event.pos[1] < 152:
            self.delete_sms()
        if event.pos[1] > 153 and event.pos[1] < 201:
            self.set_headset()
        if event.pos[1] > 251 and event.pos[1] < 303:
            self.exit = True

    def on_first_run(self):
        self.exit = False

    def delete_sms(self):
        self.fona.transmit('AT+CMGD=1,4')
        self.exit = True

    def set_headset(self):
        if self.headset:
            self.blit['surfaces'][2] = self.off
            self.headset = False
            self.fona.transmit('AT+CHFA=1')
        else:
            self.blit['surfaces'][2] = self.on
            self.headset = True
            self.fona.transmit('AT+CHFA=0')
