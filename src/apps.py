#apps.py
#Copyright (c) 2015 Tyler Spadgenske
#MIT License

import pygame, sys
from pygame.locals import *
import imp

class App():
    def __init__(self, fona):
        self.fona = fona
        #Important Variables and constants
        self.open_apps = False
        self.pixel = 0
        self.SPEED = 2
        self.opened = False
        self.close_apps = False
        self.app_to_open = None
        self.opened_app  = None
        self.blit_logo = True
        #Setup default apps
        self.get_app_order()
        self.load_logos()
        self.import_app()
        self.first_run = True

    def import_app(self):
        #Import stock apps
        loaded = []
        self.app_objects = []
        #Load modules
        for i in self.app_order:
            loaded.append(imp.load_source(i + '.Run', '/home/pi/tyos/apps/' + i +'/' + i + '.py'))
        #Load objects
        for i in loaded:
            self.app_objects.append(i.Run(self.fona))
    
    def open_app(self):
        if self.app_to_open != None:
            self.blit_logo = False
            if self.first_run or self.opened_app != self.app_to_open:
                self.opened_app = self.app_to_open
                self.app_objects[self.app_to_open].on_first_run()
                self.first_run = False
            self.app_objects[self.app_to_open].run_app() 
            if self.app_objects[self.app_to_open].exit:
                self.app_objects[self.app_to_open].exit = False
                if self.app_objects[self.app_to_open].next_app != None:
                    self.app_to_open = self.app_order.index(self.app_objects[self.app_to_open].next_app)
                else:
                    self.app_to_open = None
                    self.blit_logo = True
                self.first_run = True
            
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

        if len(order) < 4:
            print 'Not enough apps in storage!'
            pygame.quit()
            sys.exit()
        for i in range(0, len(order)):
            order[i] = order[i].rstrip()

        self.app_order = order
        
    def check(self, event):
        if event.type == MOUSEBUTTONDOWN:
            #Check for events inside of app
            if self.app_to_open != None:
                self.app_objects[self.app_to_open].get_events(event)
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
                    self.app_to_open = 0
                if event.pos[0] < 160 and event.pos[0] > 80 and event.pos[1] < 100:
                    self.app_to_open = 1
                if event.pos[0] < 240 and event.pos[0] > 160 and event.pos[1] < 100:
                    self.app_to_open = 2
                if event.pos[0] < 320 and event.pos[0] > 240 and event.pos[1] < 100:
                    self.app_to_open = 3
                
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
