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
        self.circle_image = pygame.image.load('/home/pi/tyos/apps/call/circle.png')

        num = 0
        x = 35
        y = 120
        for i in range(0, 4):
            for i in range(0, 3):
                self.circles.append(self.circle_image.get_rect())
                self.circles[num].x = x
                self.circles[num].y = y
                num += 1
                x += 90
            y += 90
            x = 35

        self.blit = {'surface':self.circle_image, 'rects':self.circles}

    def test(self):
        pass
