#apps.py
#Copyright (c) 2015 Tyler Spadgenske
#GPL License

import pygame
from pygame.locals import *

class App():
    def __init__(self):
        self.open_apps = False
        self.pixel = 0
        self.SPEED = 2
        self.opened = False
        self.close_apps = False

    def check(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.pos[1] < 31 and self.opened == False:
                self.open_apps = True
                self.close_apps = False
                self.opened = True
            if event.pos[1] > 131 and self.opened:
                self.open_apps = False
                self.close_apps = True
                self.opened = False
                
        return self.open_apps

    def open(self, update, surfaces, rects, reception, bat):
        if self.open_apps:
            update = True
            #Add one to pixels moved
            self.pixel += self.SPEED

            #Move the images
            for i in surfaces['rects']:
                i.y += self.SPEED
            for i in rects['rects']:
                i.height += self.SPEED
            for i in reception['rects']:
                i.y += self.SPEED

            bat['rects'].y += self.SPEED

            if self.pixel == 100:
                self.open_apps = False
                update = False

        if self.close_apps:
            update = True
            #Add one to pixels moved
            self.pixel -= self.SPEED

            #Move the images
            for i in surfaces['rects']:
                i.y -= self.SPEED
            for i in rects['rects']:
                i.height -= self.SPEED
            for i in reception['rects']:
                i.y -= self.SPEED

            bat['rects'].y -= self.SPEED

            if self.pixel == 0:
                self.close_apps = False
                update = False

        return update, surfaces, rects, reception, bat
