#Call App
#copyright (c) 2015 Tyler Spadgenske
#MIT License
###############################
#To be packaged with stock TYOS
###############################

import pygame

class Run():
    def __init__(self):
        self.circles = []

        #Load images
        self.circle_image = pygame.image.load('/home/pi/tyos/apps/call/circle.png')
        self.call_image = pygame.image.load('/home/pi/tyos/apps/call/call.png')
        self.back_image = pygame.image.load('/home/pi/tyos/apps/call/back.png')
        
        self.numbers = {'surfaces':[], 'rects':[]}

        #Setup colors
        self.RED = (170,0,0)
        self.WHITE = (255,255,255)
        
        #Setup fonts
        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 48)

        #Setup numbers Text
        self.number = self.font.render('1', True, self.RED, self.WHITE)
        self.number_rect = self.number.get_rect()
        
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
                
        self.blit_one_surface = {'surface':self.circle_image, 'rects':self.circles}
        self.blit = self.numbers
        
    def test(self):
        pass
