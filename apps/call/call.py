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
        self.circles = []
        self.call_number = ''
        self.call = 0
        self.exit = False
        self.ongoing_call = False
        self.first_call = True
        self.next_app = None

        self.fona = fona

        #Load images
        self.circle_image = pygame.image.load('/home/pi/tyos/apps/call/circle.png')
        self.call_image = pygame.image.load('/home/pi/tyos/apps/call/call.png')
        self.back_image = pygame.image.load('/home/pi/tyos/apps/call/back.png')
        self.hangup_image = pygame.image.load('/home/pi/tyos/apps/call/hangup.png')

        self.numbers = {'surfaces':[], 'rects':[]}

        #Setup colors
        self.RED = (170,0,0)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)

        #Setup fonts
        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 48)

        #Setup numbers Text
        self.number = self.font.render('1', True, self.RED, self.WHITE)
        self.number_rect = self.number.get_rect()

        self.call_number_text = self.font.render(self.call_number, True, self.BLACK, self.WHITE)
        self.call_number_rect = self.call_number_text.get_rect()

        num = 0
        x = 35
        y = 120
        #Setup first nine digit buttons
        for i in range(0, 3):
            for i in range(0, 3):
                self.circles.append(self.circle_image.get_rect())
                self.number = self.font.render(str(num + 1), True, self.WHITE, self.RED)
                self.numbers['surfaces'].append(self.number)
                self.numbers['rects'].append(self.number.get_rect())
                self.numbers['rects'][num].centerx = x + 35
                self.numbers['rects'][num].centery = y + 35
                self.circles[num].x = x
                self.circles[num].y = y
                num += 1
                x += 90
            y += 90
            x = 35

        #Setup 0, call, and back buttons
        self.circles.append(self.circle_image.get_rect())
        self.circles[num].x = x
        self.circles[num].y = y
        self.number = self.font.render('0', True, self.WHITE, self.RED)
        self.numbers['surfaces'].append(self.number)
        self.numbers['rects'].append(self.number.get_rect())
        self.numbers['rects'][num].centerx = x + 35
        self.numbers['rects'][num].centery = y + 35
        x += 90
        num += 1
        self.numbers['surfaces'].append(self.call_image)
        self.numbers['rects'].append(self.call_image.get_rect())
        self.numbers['rects'][num].x = x
        self.numbers['rects'][num].y = y
        x += 90
        num += 1
        self.numbers['surfaces'].append(self.back_image)
        self.numbers['rects'].append(self.back_image.get_rect())
        self.numbers['rects'][num].x = x
        self.numbers['rects'][num].y = y

        #Setup live feedback for number to be called
        self.numbers['surfaces'].append(self.call_number_text)
        self.numbers['rects'].append(self.call_number_rect)
        self.numbers['rects'][-1].x = 30
        self.numbers['rects'][-1].centery = 65

        self.blit_one_surface = {'surface':self.circle_image, 'rects':self.circles}
        self.blit = self.numbers

    def get_events(self, event):
        if self.ongoing_call == False:
            if event.pos[0] > 35 and event.pos[0] < 105:
                if event.pos[1] > 120 and event.pos[1] < 190:
                    self.call_number = self.call_number + '1'
                if event.pos[1] > 210 and event.pos[1] < 280:
                    self.call_number = self.call_number + '4'
                if event.pos[1] > 300 and event.pos[1] < 370:
                    self.call_number = self.call_number + '7'
                if event.pos[1] > 390 and event.pos[1] < 460:
                    self.call_number = self.call_number + '0'

            if event.pos[0] > 140 and event.pos[0] < 210:
                if event.pos[1] > 120 and event.pos[1] < 190:
                    self.call_number = self.call_number + '2'
                if event.pos[1] > 210 and event.pos[1] < 280:
                    self.call_number = self.call_number + '5'
                if event.pos[1] > 300 and event.pos[1] < 370:
                    self.call_number = self.call_number + '8'

            if event.pos[0] > 210 and event.pos[0] < 280:
                if event.pos[1] > 120 and event.pos[1] < 190:
                    self.call_number = self.call_number + '3'
                if event.pos[1] > 210 and event.pos[1] < 280:
                    self.call_number = self.call_number + '6'
                if event.pos[1] > 300 and event.pos[1] < 370:
                    self.call_number = self.call_number + '9'
                if event.pos[1] > 390 and event.pos[1] < 460:
                    if len(self.call_number) == 0:
                        self.exit = True
                    else:
                        self.call_number = self.call_number[:-1]

        if event.pos[0] > 140 and event.pos[0] < 210:
            if event.pos[1] > 390 and event.pos[1] < 460:
                self.call += 1
                if self.call == 2: self.call = 0

        self.blit['surfaces'][-1] = self.font.render(self.call_number, True, self.BLACK, self.WHITE)

    def call_person(self):
        if self.call == 1:
            if len(self.call_number) > 0:
                self.valid_call = True
            else:
                self.valid_call = False

            if self.valid_call:
                self.numbers['surfaces'][-3] = self.hangup_image
                self.ongoing_call = True

                if self.first_call:
                    self.fona.transmit('ATD' + self.call_number + ';') #Make call
                    self.first_call = False

            else:
                print 'Invalid Number'
                self.call = 0

        if self.ongoing_call and self.call == 0:
                self.fona.transmit('ATH')
                self.ongoing_call = False
                self.numbers['surfaces'][-3] = self.call_image
                self.exit = True
                self.first_call = True

    def run_app(self):
        self.call_person()

    def on_first_run(self):
        pass
