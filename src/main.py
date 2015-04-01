#Main.py
#Copyright (c) 2015 Tyler Spadgenske
#MIT License
VERSION = '0.1.0'

import pygame, sys, os, time, datetime
from pygame.locals import *
import framebuffer, toolbar, apps, serialport, recieve

class tyos():
    def __init__(self):
        for arg in sys.argv:
            if arg == '--power':
                self.POWER_FONA = True
                print 'Powering FONA on...'
            else:
                self.POWER_FONA = False
            
        self.VERSION = VERSION
        if self.POWER_FONA:
            import power
            power.Power().toggle()
            time.sleep(10)

        #Setup fona
        self.fona = serialport.SerialPort()
        self.fona.connect()
        #Set audio in/out to speaker and microphone
        self.fona.transmit('AT+CHFA=1')
        
        #Setup some important objects
        self.scope = framebuffer.pyscope()
        self.toolbar = toolbar.Toolbar(self.fona)
        self.apps = apps.App(self.fona)
        self.reciever = recieve.Recieve(self.fona)

        pygame.init()

        #Setup surface
        self.WINDOWWIDTH = 320
        self.WINDOWHIEGHT = 480
        self.surface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHIEGHT), pygame.FULLSCREEN)

        self.clock = pygame.time.Clock()

        #Colors        R   G   B
        self.BLUE =  (  0,  0,255)
        self.WHITE = (255,255,255)
        self.BLACK = (  0,  0,  0)

        self.surface.fill(self.WHITE)

        self.update = True

        #Setup logo
        self.logo = pygame.image.load('/home/pi/tyos/graphics/logo.png')
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.y = self.surface.get_rect().centery - 50
        self.logo_rect.centerx = self.surface.get_rect().centerx

        #Setup Battery Icon
        self.bat = pygame.image.load('/home/pi/tyos/graphics/bat.png')
        self.bat_rect = self.bat.get_rect()
        self.bat_rect.centery = 15
        self.bat_rect.right = self.WINDOWWIDTH - 10

        #Setup App Toolbar
        self.app_toolbar = pygame.Rect(0, 0, 320, 30)

        #Rectangle Dictionary
        self.rectangles = {'rects':[self.app_toolbar], 'colors':[self.BLACK]}
        #Reception Rectangle dictionary
        self.reception_bars = {'rects':[], 'colors':[]}
        #Battery Left Text
        self.bat_left = {'surface':self.toolbar.bat_left, 'rects':self.toolbar.bat_left_rect}

        #Setup fonts
        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 20)

        #Setup clock Text
        self.clock_text = self.font.render('12:00', True, self.WHITE, self.BLACK)
        self.clock_text_rect = self.clock_text.get_rect()
        self.clock_text_rect.centerx = self.surface.get_rect().centerx
        self.clock_text_rect.centery = 15

        #Image Dictionary
        self.images = {'surfaces':[self.bat], 'rects':[self.bat_rect, self.clock_text_rect]}

        self.blit_logo = True
        
    def blit_time(self):
        #Convert to 12 hour time then blit it to surface
        t = time.strftime("%H:%M")
        if int(t[0] + t[1]) > 12:
            t = str(int(t[0] + t[1]) - 12) + t[-3:]

        t = t.lstrip('0')
            
        self.clock_text = self.font.render(t, True, self.WHITE, self.BLACK)
        self.surface.blit(self.clock_text, self.images['rects'][1])
        
    def home(self):
        while True:
            #handle events and clock
            self.blit_time()
            self.handle_events()
            pygame.display.update()
            self.clock.tick()
            #Update battery and reception
            self.reception_bars, self.bat_left, self.update = self.toolbar.clock(self.reception_bars, self.bat_left,
                                                                                 self.update, self.apps.pixel)
            #Move images if necessary
            self.update, self.images, self.rectangles, self.reception_bars, self.bat_left = self.apps.open(self.update, self.images,
                                                                                              self.rectangles, self.reception_bars,
                                                                                              self.bat_left)
            #Open app if tapped
            self.apps.open_app()

            #Check for calls and sms
            self.update = self.reciever.check(self.update)
            
            #Update if necessary
            if self.update:
                self.blit(self.images, self.rectangles, self.reception_bars, self.bat_left)
                self.update = False
                    
    def blit(self, surfaces, rects, reception, bat):
        self.surface.fill(self.WHITE)

        if self.apps.app_to_open != None:
            self.blit_logo = False
            #Blit images using one image but different rectangles
            for i in self.apps.app_objects[self.apps.app_to_open].blit_one_surface['rects']:
                self.surface.blit(self.apps.app_objects[self.apps.app_to_open].blit_one_surface['surface'], i)
            #Blit images using multiple images and rectangles
            for rect, surface in zip(self.apps.app_objects[self.apps.app_to_open].blit['rects'],
                                        self.apps.app_objects[self.apps.app_to_open].blit['surfaces']):
                self.surface.blit(surface, rect)
                
        #Blit all rectangles
        for rect, color in zip(rects['rects'], rects['colors']):
            pygame.draw.rect(self.surface, color, rect)

        #Blit all reception bars
        for rect, color in zip(reception['rects'], reception['colors']):
            pygame.draw.rect(self.surface, color, rect)

        #Blit all images
        for surface, rect in zip(surfaces['surfaces'], surfaces['rects']):
            self.surface.blit(surface, rect)

        #Blit battery Percentage
        self.surface.blit(bat['surface'], bat['rects'])
        
        #Blit logo
        if self.apps.blit_logo:
            self.surface.blit(self.logo, self.logo_rect)

        if self.apps.logos['rects'][0].y != -50:
            for surface, rect in zip(self.apps.logos['surfaces'], self.apps.logos['rects']):
                self.surface.blit(surface, rect)

        #Blit incoming call
        if self.reciever.call_coming:
            for surface, rect in zip(self.reciever.blit['surfaces'], self.reciever.blit['rects']):
                    self.surface.blit(surface, rect)

    def handle_events(self):
        for event in pygame.event.get():
            self.update = True
            self.apps.update_app = True
            self.app_bar = self.apps.check(event)
            if self.reciever.call_coming:
                self.reciever.get_events(event)
                
phone = tyos()
try:
    phone.home()
    
except KeyboardInterrupt:
    print
    print 'Closing TYOS ' + phone.VERSION
    if phone.POWER_FONA:
        power.Power().toggle()
    pygame.quit()
    sys.exit()
