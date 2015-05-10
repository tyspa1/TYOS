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

        #Define images
        self.shutdown_image = pygame.image.load('/home/pi/tyos/apps/power/shutdown.png')
        self.shutdown_rect = self.shutdown_image.get_rect()
        self.shutdown_rect.centerx = 160
        self.shutdown_rect.centery = 240
        
        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit = {'surfaces':[self.shutdown_image], 'rects':[self.shutdown_rect]}
        self.next_app = None

    def run_app(self):
        pass

    def get_events(self, event):
        if event.pos[0] > 60 and event.pos[0] < 260:
            if event.pos[1] > 134 and event.pos[1] < 200:
                print 'Shutting Down TYOS'
                self.shutdown()
            if event.pos[1] > 200 and event.pos[1] < 272:
                print 'Logging Out of TYOS'
                self.logout()
            if event.pos[1] > 272 and event.pos[1] < 344:
                self.exit = True

    def shutdown(self):
        os.system('sudo python /home/pi/tyos/src/power.py') #Power off fona
        pygame.quit()
        time.sleep(1)
        a = Popen(['sudo', 'halt']) #Power down Raspberry Pi
        sys.exit()

    def logout(self):
        pygame.quit()
        time.sleep(1)
        sys.exit()

    def on_first_run(self):
        pass
