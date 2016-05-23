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
from subprocess import Popen

class Stream():
    def __init__(self):
        self.mode = 'capture'
        self.deleted = False
        self.uploading = False
        self.no_files = False
        #Get current photo name index
        try:
            index_file = open('/home/pi/index.dat', 'r')
        except:
            #Create new file if needed
            index_file = open('/home/pi/index.dat', 'w+')
            index_file.write('0')
            index_file.close()
            index_file = open('/home/pi/index.dat')
            print 'NO INDEX FILE. CREATED /home/pi/index.dat'
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

        #Setup buttons
        self.capture = pygame.image.load('/home/pi/tyos/apps/camera/camera.png')
        self.gallery = pygame.image.load('/home/pi/tyos/apps/camera/images/gallery.png')
        self.door = pygame.image.load('/home/pi/tyos/apps/camera/images/door.png')
        self.right = pygame.image.load('/home/pi/tyos/apps/camera/images/right.png')
        self.left = pygame.image.load('/home/pi/tyos/apps/camera/images/left.png')
        self.home = pygame.image.load('/home/pi/tyos/apps/camera/images/home.png')
        self.upload = pygame.image.load('/home/pi/tyos/apps/camera/images/upload.png')
        self.delete = pygame.image.load('/home/pi/tyos/apps/camera/images/trash.png')
        self.deleted_image = pygame.image.load('/home/pi/tyos/apps/camera/images/deleted.png')
        self.uploading_image = pygame.image.load('/home/pi/tyos/apps/camera/images/uploading.png')
        self.no_files_image = pygame.image.load('/home/pi/tyos/apps/camera/images/nofiles.png')
        
    def display(self):
        while True:
            if self.mode == 'gallery':                        
                self.screen.blit(self.image_in_view, (0,0))
                self.screen.blit(self.left, (20, 410))
                self.screen.blit(self.right, (240, 410))
                self.screen.blit(self.home, (125, 400))
                self.screen.blit(self.delete, (5, 5))
                self.screen.blit(self.upload, (40, 5))
                if self.deleted:
                    self.screen.blit(self.deleted_image, (79, 200))
                    if time.time() - self.delete_time > 3:
                        self.deleted = False
                if self.uploading:
                    self.screen.blit(self.uploading_image, (79, 200))
                    if time.time() - self.uploading_time > 6:
                        self.uploading = False
                
            if self.mode == 'capture':
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
                self.screen.blit(self.gallery, (20, 415))
                self.screen.blit(self.door, (240, 410))

                if self.no_files:
                    self.screen.blit(self.no_files_image, (79, 200))
                    if time.time() - self.files_time > 3:
                        self.no_files = False
            
            pygame.display.update()
            
            #Handle events
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.mode == 'gallery':
                        if event.pos[1] < 40 and event.pos[0] < 35:
                            self.deleted = True
                            self.delete_time = time.time()
                            os.remove('/home/pi/Photos/' + self.images[self.current_image])
                            self.current_image = 0
                            self.images = os.listdir('/home/pi/Photos/')
                            if len(self.images) == 0:
                                self.mode = 'capture'
                                self.no_files = True
                                self.files_time = time.time()
                            
                        if event.pos[1] < 40 and event.pos[0] > 35 and event.pos[0] < 75:
                            self.uploading = True
                            self.uploading_time = time.time()
                            cam = Popen(['/home/pi/Dropbox-Uploader/./dropbox_uploader.sh', 'upload', '/home/pi/Photos/' +
                                         self.images[self.current_image], self.images[self.current_image]])
                            
                    if event.pos[1] > 400 and event.pos[1] < 470:
                        if event.pos[0] > 125 and event.pos[0] < 195:
                            if self.mode == 'capture':
                                self.camera.capture('/home/pi/Photos/' + str(self.index) + '.jpg')
                                self.index += 1
                            if self.mode == 'gallery':
                                self.mode = 'capture'
            
                        if event.pos[0] < 70:
                            if self.mode == 'capture':
                                self.mode = 'gallery'
                                self.current_image = 0
                                self.images = os.listdir('/home/pi/Photos/')
                                if len(self.images) == 0:
                                    self.mode = 'capture'
                                    self.no_files = True
                                    self.files_time = time.time()
                                else:
                                    self.image_in_view = pygame.image.load('/home/pi/Photos/' + self.images[self.current_image])
                                
                            if self.mode == 'gallery':
                                self.current_image -= 1
                                if self.current_image == -1:
                                    self.current_image = len(self.images) - 1
                                self.image_in_view = pygame.image.load('/home/pi/Photos/' + self.images[self.current_image])
                                
                        if event.pos[0] > 255:
                            if self.mode == 'capture':
                                print 'exiting...'
                                os.remove('/home/pi/index.dat')
                                new = open('/home/pi/index.dat', 'w+')
                                new.write(str(self.index))
                                new.close()
                                cam = Popen(['sudo', 'python', '/home/pi/tyos/src/main.py'])
                                pygame.quit()
                                sys.exit()


                            if self.mode == 'gallery':
                                if self.current_image == len(self.images) - 1:
                                    self.current_image = 0
                                else:
                                    self.current_image += 1
                                self.image_in_view = pygame.image.load('/home/pi/Photos/' + self.images[self.current_image])
            
if __name__ == '__main__':
    q = Stream()
    q.display()
