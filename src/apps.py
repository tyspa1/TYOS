#apps.py
#Copyright (c) 2015 Tyler Spadgenske
#GPL License

import pygame
from pygame.locals import *

class App():
    def __init__(self):
        #Important Variables and constants
        self.open_apps = False
        self.pixel = 0
        self.SPEED = 2
        self.opened = False
        self.close_apps = False
        self.app_to_open = 0
        
        #Setup default apps
        self.get_app_order()
        self.load_logos()

    def load_logos(self):
        #Load the first four app's logo
        logos = {'surfaces':[], 'rects':[]}
        for i in range(0, 4):
            logos['surfaces'].append(pygame.image.load('/home/pi/tyos/apps/' + self.app_order[i] + '/' + self.app_order[i] + '.png'))
            logos['rects'].append(logos['surfaces'][i].get_rect())

        for i in range(0, 4):
            logos['rects'][i].centery = -50
            logos['rects'][i].centerx = 40 + 80 * i

        self.logos = logos
        
    def get_app_order(self):
        #Get the order of the apps to be blitted
        order_file = open('/home/pi/tyos/apps/order.txt', 'r')
        order = order_file.readlines()

        for i in range(0, len(order)):
            order[i] = order[i].rstrip()

        self.app_order = order
        
    def check(self, event):
        if event.type == MOUSEBUTTONDOWN:
            #Check for touch to open apps bar
            if event.pos[1] < 31 and self.opened == False:
                self.open_apps = True
                self.close_apps = False
                self.opened = True
            #Check for touch to close app bar
            if event.pos[1] > 131 and self.opened:
                self.open_apps = False
                self.close_apps = True
                self.opened = False
            #Check for touch to open an app
            if self.opened and self.logos['rects'][0].centery == 50:
                if event.pos[0] < 80 and event.pos[1] < 100:
                    self.app_to_open = 1
                if event.pos[0] < 160 and event.pos[0] > 80 and event.pos[1] < 100:
                    self.app_to_open = 2
                if event.pos[0] < 240 and event.pos[0] > 160 and event.pos[1] < 100:
                    self.app_to_open = 3
                if event.pos[0] < 320 and event.pos[0] > 240 and event.pos[1] < 100:
                    self.app_to_open = 4

                print self.app_to_open
                
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
            for i in self.logos['rects']:
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
            for i in self.logos['rects']:
                i.y -= self.SPEED

            bat['rects'].y -= self.SPEED

            if self.pixel == 0:
                self.close_apps = False
                update = False

        return update, surfaces, rects, reception, bat

if __name__ == '__main__':
    t = App()
    t.get_app_order()
