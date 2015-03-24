#Main.py
#Copyright (c) 2015 Tyler Spadgenske
#GPL License
VERSION = '0.1.0'

import pygame, sys, os
from pygame.locals import *
import framebuffer

class tyfone():
    def __init__(self):
        self.VERSION = VERSION

        self.scope = framebuffer.pyscope()
        pygame.init()

        self.WINDOWWIDTH = 320
        self.WINDOWHIEGHT = 480

        self.surface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHIEGHT), pygame.FULLSCREEN)

        self.clock = pygame.time.Clock()

        self.BLUE = (0,0,255)
        self.WHITE = (255, 255, 255)

        self.surface.fill(self.WHITE)

        self.update = True

        #Setup logo
        self.logo = pygame.image.load('/home/pi/tyos/graphics/logo.png')
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.y = self.surface.get_rect().centery - 50
        self.logo_rect.centerx = self.surface.get_rect().centerx 

    def home(self):
        while True:
            self.handle_events()
            pygame.display.update()
            self.clock.tick()

            if self.update:
                self.blit([self.logo], [self.logo_rect])
                self.update = False

    def blit(self, surfaces, rects):
        for surface, rect in zip(surfaces, rects):
            self.surface.blit(surface, rect)

    def handle_events(self):
        for event in pygame.event.get():
            self.update = True
            if event.type == MOUSEBUTTONDOWN:
                pass
                
                
tyos = tyfone()
try:
    tyos.home()
    
except KeyboardInterrupt:
    print
    print 'Closing TYOS ' + tyos.VERSION
    pygame.quit()
    sys.exit()
