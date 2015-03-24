#Main.py
#Copyright (c) 2015 Tyler Spadgenske
#GPL License
VERSION = '0.1.0'

import pygame, sys, os
from pygame.locals import *
import framebuffer, toolbar

class tyfone():
    def __init__(self):
        self.VERSION = VERSION

        self.scope = framebuffer.pyscope()
        self.toolbar = toolbar.Toolbar()
        pygame.init()

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

        #Setup App Toolbar
        self.app_toolbar = pygame.Rect(0, 0, 320, 30)

        #Image Dictionary
        self.images = {'surfaces':[self.logo], 'rects':[self.logo_rect]}
        #Rectangle Dictionary
        self.rectangles = {'rects':[self.app_toolbar], 'colors':[self.BLACK]}
        
    def home(self):
        #TODO: Remove when toolbar.clock() is done
        self.rectangles = self.toolbar.check_reception(self.rectangles)
        
        while True:
            #handle events and clock
            self.handle_events()
            pygame.display.update()
            self.clock.tick()

            #Update if neccesary
            if self.update:
                self.blit(self.images['surfaces'], self.images['rects'], self.rectangles['rects'], self.rectangles['colors'])
                self.update = False

    def blit(self, surfaces, sur_rects, rects, colors):
        #Blit all images
        for surface, rect in zip(surfaces, sur_rects):
            self.surface.blit(surface, rect)

        #Blit all rectangles
        for rect, color in zip(rects, colors):
            pygame.draw.rect(self.surface, color, rect)
            

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
