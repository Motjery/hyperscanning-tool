#! /usr/bin/python
# coding: utf-8

import wiiboard
# import client_2
import pygame
import time
import curses
import threading
import socket
import pygame.gfxdraw
from pygame.locals import *

host = '10.216.25.133'
port = 50000


# class ThreadEmission(threading.Thread):
#    """objet thread gérant l'émission des messages"""#

#    def __init__(self, conn):
#        threading.Thread.__init__(self)
#        self.connexion = conn           # réf. du socket de connexion#

#    def run(self):
#        while 1:
#            message_emis = raw_input()
#            self.connexion.send(message_emis)

def main():

    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host, port))
    except socket.error:
        print "La connexion a echoue."
        sys.exit()
    print "Connexion etablie avec le serveur."
  #  if(raw_input == "exit"):
#        connexion.close()
#    th_E = ThreadEmission(connexion)
#    th_E.start()

#
    # initialization wiifit
    board = wiiboard.Wiiboard()
    pygame.init()
    address = board.discover()
    board.connect(address)  # The wii board must be in sync mode at this time#
    # initializations
    time.sleep(0.1)
    board.setLight(True)
    done = False
    time_limit = 60
    weight_threshold = 4
    recording = False
    # MAIN LOOP
    while (not done):
        time.sleep(0.05)
        for event in pygame.event.get():
            str(pygame.event.get())
            if event.type == wiiboard.WIIBOARD_MASS:
                if (event.mass.totalWeight > weight_threshold):
                    # time.sleep(0.05)
                    if recording:
                        total = event.mass.totalWeight
                        x = ((event.mass.topRight + event.mass.bottomRight) - (event.mass.topLeft + event.mass.bottomLeft)
                             ) / total
                        y = ((event.mass.bottomRight + event.mass.bottomLeft) - (event.mass.topRight + event.mass.topLeft)
                             ) / total 
                        time.sleep(0.001)
                        pos = (`x`+',' + `y`+'|')
                        print pos
                        if x is not None and x is not '':
							if y is not None and y is not '':
							    connexion.send(pos)
							    t=time.time()-init_time
							    save_name="test.csv"
							    save=open(save_name,"a")
							    save.write(`t`+','+`x`+','+`y`+'\n')
                        time.sleep(0.001)

                        # End of recording ?
                        if ((time.time() - init_time) > time_limit):
                            recording = False
                            print "End of recording"
            # The BUTTON event activates recording
            elif event.type == wiiboard.WIIBOARD_BUTTON_PRESS:
                print "Bouton devant"
                print "Button pressed!"
            elif event.type == wiiboard.WIIBOARD_BUTTON_RELEASE:
                if not recording:
                    print "Bouton inconnu"
                    print "Button released -> recording...."
                    init_time = time.time()
                    recording = True
                elif recording:
                    recording = False
                    init_time = time.time()
                    recording = True
            # Press any key on the computer keyboard to quit
            elif event.type == QUIT:
                print "Quit !"
                # output_file.close()
                done = True
                pygame.display.update()
            # Other event types:
            # wiiboard.WIIBOARD_CONNECTED
            # wiiboard.WIIBOARD_DISCONNECTED
    pygame.quit()
    board.disconnect()
    sys.exit()



# Run the script if executed
if __name__ == "__main__":
    main()
