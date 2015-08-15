#Camera App
#copyright (c) 2015 Tyler Spadgenske
# MIT License

import sys
import pygame
import picamera
import io
import yuv2rgb
import os
import time

class Stream():
    def __init__(self):
        #Get current photo name index
        try:
            index_file = open('/home/pi/tyos/apps/camera/index.dat', 'r')
        except:
            #Create new file if needed
            index_file = open('/home/pi/tyos/apps/camera/index.dat', 'w+')
            index_file.write('0')
            index_file.close()
            index_file = open('/home/pi/tyos/apps/camera/index.dat')
            print 'NO INDEX FILE. CREATED /home/pi/tyos/apps/camera/index.dat'
        self.index = int(index_file.readline())
        index_file.close()
        
        #Set screen to SPI
        os.environ["SDL_FBDEV"] = "/dev/fb1"
        os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen" #Use touchscreen instead of event0
        os.environ["SDL_MOUSEDRV"] = "TSLIB"

        #COnfigure camera
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 480)
        self.camera.rotation = 90
        
        # Buffers for viewfinder data
        self.rgb = bytearray(320 * 480 * 3)
        self.yuv = bytearray(320 * 480 * 3 / 2)

        #Setup window
        self.screen = pygame.display.set_mode((320, 480), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)

        #Setup capture button
        self.capture = pygame.image.load('/home/pi/tyos/apps/camera/camera.png')
        
    def display(self):
        while True:
            #Get camera stream
            self.stream = io.BytesIO() # Capture into in-memory stream
            self.camera.capture(self.stream, use_video_port=True, format='raw')
            self.stream.seek(0)
            self.stream.readinto(self.yuv)  # stream -> YUV buffer
            self.stream.close()
            yuv2rgb.convert(self.yuv, self.rgb, 320, 480)
            
            #Create pygame image from screen and blit it
            img = pygame.image.frombuffer(self.rgb[0:(320 * 480 * 3)], (320, 480), 'RGB')
            self.screen.blit(img, (0,0))

            #Blit buttons
            self.screen.blit(self.capture, (125, 400))

            pygame.display.update()
            
            #Handle events
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.pos[0] > 125 and event.pos[0] < 195 and event.pos[1] > 400 and event.pos[1] < 470:
                        self.camera.capture('/home/pi/Photos/' + str(self.index) + '.jpg')
                        self.index += 1
            
if __name__ == '__main__':
    q = Stream()
    q.display()
