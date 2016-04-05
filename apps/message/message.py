#Message App
#copyright (c) 2015 Tyler Spadgenske
#MIT License
################################
#To be packaged with stock TYOS#
################################

import pygame, time, os
from pygame.locals import *

class Run():
    def __init__(self, fona):
        self.fona = fona
        self.next_app = None

        #Colors
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.send = False
        self.valid = False

        #Variables
        self.mode = 3
        self.number = ''
        self.message = ''
        self.first = False

        self.sms_messages = {'messages':[], 'senders':[]}
        self.page = 1

        #Load images
        self.keyboard_image = pygame.image.load('/home/pi/tyos/apps/message/keyboard.png')
        self.num_keyboard_image = pygame.image.load('/home/pi/tyos/apps/message/numbered_keyboard.png')
        self.bubble = pygame.image.load('/home/pi/tyos/apps/message/bubble.png')
        self.keyboard_rect = self.keyboard_image.get_rect()
        self.keyboard_rect.x = 6
        self.keyboard_rect.y = 293

        #Main conversation image
        self.conversation_image = pygame.image.load('/home/pi/tyos/apps/message/conversation.png')
        self.conversation_rect = self.conversation_image.get_rect()
        self.conversation_rect.centerx = 160
        self.conversation_rect.centery = 260

        #Setup text
        #Setup fonts
        self.font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 20)
        self.message_font = pygame.font.Font('/home/pi/tyos/fonts/arial.ttf', 12)

        #please wait Text
        self.wait = self.font.render('Please wait...', True, self.BLACK, self.WHITE)
        self.wait_rect = self.wait.get_rect()
        self.wait_rect.centerx = 160
        self.wait_rect.centery = 240

        #Says... text
        self.says_text1 = self.font.render('Tyler says...', True, self.BLACK, self.WHITE)
        self.says_rect1 = self.says_text1.get_rect()
        self.says_rect1.x = 35
        self.says_rect1.y = 120
        self.says_text2 = self.font.render('Billy says...', True, self.BLACK, self.WHITE)
        self.says_rect2 = self.says_text2.get_rect()
        self.says_rect2.x = 35
        self.says_rect2.y = 233

        #Message lines
        self.message_line1 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message_line1_rect = self.message_line1.get_rect()
        self.message_line1_rect.x = 42
        self.message_line1_rect.y = 155
        self.message_line2 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message_line2_rect = self.message_line2.get_rect()
        self.message_line2_rect.x = 42
        self.message_line2_rect.y = 177
        self.message_line3 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message_line3_rect = self.message_line3.get_rect()
        self.message_line3_rect.x = 42
        self.message_line3_rect.y = 199

        self.message2_line1 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message2_line1_rect = self.message2_line1.get_rect()
        self.message2_line1_rect.x = 42
        self.message2_line1_rect.y = 270
        self.message2_line2 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message2_line2_rect = self.message2_line2.get_rect()
        self.message2_line2_rect.x = 42
        self.message2_line2_rect.y = 293
        self.message2_line3 = self.font.render('', True, self.BLACK, self.WHITE)
        self.message2_line3_rect = self.message2_line3.get_rect()
        self.message2_line3_rect.x = 42
        self.message2_line3_rect.y = 316

        #Number to send
        #Setup numbers Text
        self.number_text = self.font.render(self.number, True, self.BLACK, self.WHITE)
        self.number_rect = self.number_text.get_rect()
        self.number_rect.x = 15
        self.number_rect.y = 57

        #Setup numbers Text
        self.line1 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line1_rect = self.line1.get_rect()
        self.line1_rect.x = 15
        self.line1_rect.y = 130

        #Setup numbers Text
        self.line2 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line2_rect = self.line2.get_rect()
        self.line2_rect.x = 15
        self.line2_rect.y = 150

        #Setup numbers Text
        self.line3 = self.font.render(self.message, True, self.BLACK, self.WHITE)
        self.line3_rect = self.line3.get_rect()
        self.line3_rect.x = 15
        self.line3_rect.y = 170

        self.bubble_rect = self.bubble.get_rect()
        self.bubble_rect.x = 5
        self.bubble_rect.y = 50

        #Stuff to follow app protocol
        self.exit = False
        self.blit_one_surface = {'surface':[], 'rects':[]}
        self.blit_mode1 = {'surfaces':[self.keyboard_image, self.bubble, self.line1, self.line2,
                                 self.line3, self.number_text], 'rects':[self.keyboard_rect, self.bubble_rect, self.line1_rect, self.line2_rect,
                                                       self.line3_rect, self.number_rect]}
        self.blit_mode2 = {'surfaces':[self.conversation_image, self.says_text1, self.says_text2, self.message_line1,
                                       self.message_line2, self.message_line3,
                                       self.message2_line1, self.message2_line2,
                                       self.message2_line3], 'rects':[self.conversation_rect,
                                                                                           self.says_rect1, self.says_rect2,
                                                                      self.message_line1_rect, self.message_line2_rect,
                                                                      self.message_line3_rect, self.message2_line1_rect,
                                                                       self.message2_line2_rect,self.message2_line3_rect]}
        self.blit_mode3 = {'surfaces':[self.wait], 'rects':[self.wait_rect]}
        self.blit = self.blit_mode2
        self.load_contacts()

    def load_contacts(self):
        self.contacts = {'names':[], 'numbers':[]}
        try:
            contact_file = open('/home/pi/tyos/configure/contacts.conf', 'r')
        except:
            print '***********************************************************'
            print 'NO CONTACTS FOUND'
            print 'PLEASE EDIT /home/pi/tyos/configure/contacts.conf FILE'
            print '***********************************************************'
            if not os.path.exists('/home/pi/tyos/configure'):
                os.mkdir('/home/pi/tyos/configure')
            if not os.path.exists('/home/pi/tyos/logs'):
                os.mkdir('/home/pi/tyos/logs') #May be in wrong spot, but it works
            contact_file = open('/home/pi/tyos/configure/contacts.conf', 'w+')
            contact_file.write('#Contacts\n')
            contact_file.write('#Use format name=number i.e. Joe=1555666777 # are comments\n')
            contact_file.close()
            contact_file = open('/home/pi/tyos/configure/contacts.conf', 'r')

        self.contact_list = contact_file.readlines()
        contact_file.close()

        for i in range(0, len(self.contact_list)):
            if self.contact_list[i][0] == '#':
                pass
                #Do Nothing. Line is comment
            else:
                self.contact_list[i] = self.contact_list[i].rstrip().split('=')

    def on_first_run(self):
        self.first = False
        self.mode = 3

    def get_sms(self):
        #Set to text mode
        self.fona.transmit('AT+CMGF=1')
        self.fona.transmit('AT+CSDH=1')
        #Get number of sms messages
        num_sms = self.fona.transmit('AT+CPMS?')
        num_sms = num_sms[1]
        num_sms = num_sms.split(',')
        num_sms = num_sms[1]
        print 'SMS FOUND IN MEMORY: ' + num_sms
        print 'LOADING SMS MESSAGES...'
        #Retrieve sms messages
        for i in range(1, int(num_sms) + 1):
            self.sms_messages['senders'].append(self.fona.transmit('AT+CMGR=' + str(i))[1].split('"')[3].replace('+',''))
            self.sms_messages['messages'].append(self.fona.transmit('AT+CMGR=' + str(i))[2])

        #If in contacts, replace number with name
        for i in self.contact_list:
            index = 0
            for senders in self.sms_messages['senders']:
                if i[1] == senders:
                    self.sms_messages['senders'][index] = i[0]
                index += 1

        #If there are less than two messages, do some configuring
        if int(num_sms) < 2:
            self.sms_messages['senders'].append('')
            self.sms_messages['messages'].append('')
            if int(num_sms) == 0:
                self.sms_messages['senders'].append('')
                self.sms_messages['messages'].append('')

    def config_sms(self):
        self.blit['surfaces'][1] = self.font.render(self.sms_messages['senders'][(self.page + 1) * -1] + ' says...', True, self.BLACK, self.WHITE)
        self.blit['surfaces'][2] = self.font.render(self.sms_messages['senders'][self.page * -1] + ' says...', True, self.BLACK, self.WHITE)
        #Box 1
        self.blit['surfaces'][3] = self.font.render(self.sms_messages['messages'][(self.page + 1) * -1][:25], True, self.BLACK, self.WHITE)
        if len(self.sms_messages['messages'][(self.page + 1) * -1]) > 25:
            self.blit['surfaces'][4] = self.font.render(self.sms_messages['messages'][(self.page + 1)* -1][25:50], True, self.BLACK, self.WHITE)
            if len(self.sms_messages['messages'][(self.page + 1) * -1]) > 50:
                self.blit['surfaces'][5] = self.font.render(self.sms_messages['messages'][(self.page + 1)* -1][50:75], True, self.BLACK, self.WHITE)
            else:
                self.blit['surfaces'][5] = self.font.render('', True, self.BLACK, self.WHITE)
        else:
            self.blit['surfaces'][4] = self.font.render('', True, self.BLACK, self.WHITE)
            self.blit['surfaces'][5] = self.font.render('', True, self.BLACK, self.WHITE)

        #Box 2
        self.blit['surfaces'][6] = self.font.render(self.sms_messages['messages'][self.page * -1][:25], True, self.BLACK, self.WHITE)
        if len(self.sms_messages['messages'][self.page * -1]) > 25:
            self.blit['surfaces'][7] = self.font.render(self.sms_messages['messages'][self.page * -1][25:50], True, self.BLACK, self.WHITE)
            if len(self.sms_messages['messages'][self.page * -1]) > 50:
                self.blit['surfaces'][8] = self.font.render(self.sms_messages['messages'][self.page * -1][50:75], True, self.BLACK, self.WHITE)
            else:
                self.blit['surfaces'][8] = self.font.render('', True, self.BLACK, self.WHITE)
        else:
            self.blit['surfaces'][7] = self.font.render('', True, self.BLACK, self.WHITE)
            self.blit['surfaces'][8] = self.font.render('', True, self.BLACK, self.WHITE)

    def run_app(self):
        if self.mode == 3:
            self.blit = self.blit_mode3
            if self.first:
                time.sleep(5)
                self.mode = 2
                self.blit = self.blit_mode2
                self.sms_messages = {'messages':[], 'senders':[]}
                self.get_sms()
                self.config_sms()
            self.first = True

        if self.exit:
            self.mode = 2
        if len(self.number) > 0:
            self.valid = True
        else:
            self.valid = False
            self.send = False
        if self.send and self.valid:
            self.send = False
            self.valid = False
            self.fona.transmit('AT+CMGF=1')
            time.sleep(.25)
            self.fona.transmit('AT+CMGS="' + self.number + '"')
            time.sleep(0.25)
            self.fona.transmit(self.message)
            time.sleep(.25)
            self.fona.transmit(chr(26))
            self.mode = 2
            self.blit = self.blit_mode2

    def get_events(self, event):
        if self.mode != 2:
            self.get_keyboard_events(event)
        else:
            self.get_read_events(event)

    def get_read_events(self, event):
        if event.pos[0] > 35 and event.pos[0] < 285:
            if event.pos[1] > 62 and event.pos[1] < 105:
                self.page += 1
                if self.page == len(self.sms_messages['senders']):
                    self.page = len(self.sms_messages['senders']) - 1
                self.config_sms()

            if event.pos[1] > 352 and event.pos[1] < 403:
                self.page -= 1
                if self.page == 0:
                    self.page = 1
                self.config_sms()
            if event.pos[1] > 410 and event.pos[1] < 455:
                self.mode = 0
                self.blit = self.blit_mode1

    def get_keyboard_events(self, event):
        #Get key pressed
        #Row 1
        if event.pos[1] > 290 and event.pos[1] < 330:
            if event.pos[0] > 6 and event.pos[0] < 31:
                if self.mode == 1:
                    self.message = self.message + 'q'
                else:
                    self.number = self.number + '1'
            if event.pos[0] > 37 and event.pos[0] < 62:
                if self.mode == 1:
                    self.message = self.message + 'w'
                else:
                    self.number = self.number + '2'
            if event.pos[0] > 68 and event.pos[0] < 93:
                if self.mode == 1:
                    self.message = self.message + 'e'
                else:
                    self.number = self.number + '3'
            if event.pos[0] > 99 and event.pos[0] < 124:
                if self.mode == 1:
                    self.message = self.message + 'r'
                else:
                    self.number = self.number + '4'
            if event.pos[0] > 130 and event.pos[0] < 155:
                if self.mode == 1:
                    self.message = self.message + 't'
                else:
                    self.number = self.number + '5'
            if event.pos[0] > 161 and event.pos[0] < 186:
                if self.mode == 1:
                    self.message = self.message + 'y'
                else:
                    self.number = self.number + '6'
            if event.pos[0] > 192 and event.pos[0] < 217:
                if self.mode == 1:
                    self.message = self.message + 'u'
                else:
                    self.number = self.number + '7'
            if event.pos[0] > 223 and event.pos[0] < 248:
                if self.mode == 1:
                    self.message = self.message + 'i'
                else:
                    self.number = self.number + '8'
            if event.pos[0] > 254 and event.pos[0] < 279:
                if self.mode == 1:
                    self.message = self.message + 'o'
                else:
                    self.number = self.number + '9'
            if event.pos[0] > 285 and event.pos[0] < 310:
                if self.mode == 1:
                    self.message = self.message + 'p'
                else:
                    self.number = self.number + '0'
        #Row 2
        if event.pos[1] > 336 and event.pos[1] < 376:
            if event.pos[0] > 18 and event.pos[0] < 43:
                if self.mode == 1:
                    self.message = self.message + 'a'
            if event.pos[0] > 49 and event.pos[0] < 74:
                if self.mode == 1:
                    self.message = self.message + 's'
            if event.pos[0] > 80 and event.pos[0] < 115:
                if self.mode == 1:
                    self.message = self.message + 'd'
            if event.pos[0] > 111 and event.pos[0] < 136:
                if self.mode == 1:
                    self.message = self.message + 'f'
            if event.pos[0] > 142 and event.pos[0] < 167:
                if self.mode == 1:
                    self.message = self.message + 'g'
            if event.pos[0] > 173 and event.pos[0] < 198:
                if self.mode == 1:
                    self.message = self.message + 'h'
            if event.pos[0] > 204 and event.pos[0] < 229:
                if self.mode == 1:
                    self.message = self.message + 'j'
            if event.pos[0] > 235 and event.pos[0] < 260:
                if self.mode == 1:
                    self.message = self.message + 'k'
            if event.pos[0] > 266 and event.pos[0] < 291:
                if self.mode == 1:
                    self.message = self.message + 'l'
        #Row 3
        if event.pos[1] > 382 and event.pos[1] < 422:
            if event.pos[0] > 49 and event.pos[0] < 74:
                if self.mode == 1:
                    self.message = self.message + 'z'
            if event.pos[0] > 80 and event.pos[0] < 115:
                if self.mode == 1:
                    self.message = self.message + 'x'
            if event.pos[0] > 111 and event.pos[0] < 136:
                if self.mode == 1:
                    self.message = self.message + 'c'
            if event.pos[0] > 142 and event.pos[0] < 167:
                if self.mode == 1:
                    self.message = self.message + 'v'
            if event.pos[0] > 173 and event.pos[0] < 198:
                if self.mode == 1:
                    self.message = self.message + 'b'
            if event.pos[0] > 204 and event.pos[0] < 229:
                if self.mode == 1:
                    self.message = self.message + 'n'
            if event.pos[0] > 235 and event.pos[0] < 260:
                if self.mode == 1:
                    self.message = self.message + 'm'
        #Row 4
        if event.pos[1] > 428 and event.pos[1] < 468:
            if event.pos[0] > 49 and event.pos[0] < 115:
                if self.mode == 1:
                    self.message = self.message[:-1]
                else:
                    self.number = self.number[:-1]
            if event.pos[0] > 111 and event.pos[0] < 198:
                if self.mode == 1:
                    self.message = self.message + ' '
            if event.pos[0] > 204 and event.pos[0] < 260:
                self.send = True

        #Keyboard mode
        if event.pos[0] > 5 and event.pos[0] < 318 and event.pos[1] > 50 and event.pos[1] < 78:
            self.mode = 0
        if event.pos[0] > 5 and event.pos[0] < 318 and event.pos[1] > 88 and event.pos[1] < 218:
            self.mode = 1

        if self.mode == 0:
            self.blit['surfaces'][0] = self.num_keyboard_image
        else:
            self.blit['surfaces'][0] = self.keyboard_image

        self.blit['surfaces'][2] = self.font.render(self.message[:32], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][3] = self.font.render(self.message[32:64], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][4] = self.font.render(self.message[64:96], True, self.BLACK, self.WHITE)
        self.blit['surfaces'][5] = self.font.render(self.number, True, self.BLACK, self.WHITE)
