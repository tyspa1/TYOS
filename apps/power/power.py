#Call App
#copyright (c) 2015 Tyler Spadgenske
#MIT License
###############################
#To be packaged with stock TYOS
###############################

import os, time, sys, pygame
from subprocess import Popen

class Run():
    def __init__(self, fona):
        self.POWER_DOWN = False
        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit = {'surfaces':[], 'rects':[]}

    def run_app(self):
        if self.POWER_DOWN:
            os.system('sudo python /home/pi/tyos/src/power.py') #Power off fona
        pygame.quit()
        time.sleep(1)
        if self.POWER_DOWN:
            a = Popen(['sudo', 'halt']) #Power down Raspberry Pi
        sys.exit()

    def get_events(self, event):
        pass
