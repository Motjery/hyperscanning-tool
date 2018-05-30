#! /usr/bin/env python

import wiiboard
import pygame
import time
import curses
import pygame.gfxdraw
from pygame.locals import *

def main():
    board = wiiboard.Wiiboard()

    pygame.init()
    address = board.discover()
    board.connect(address)  # The wii board must be in sync mode at this time

    # initializations
    time.sleep(0.1)
    board.setLight(True)
    done = False
    time_limit = 40
    weight_threshold = 4
    recording = False
    screen = curses.initscr()

    # MAIN LOOP
    while (not done):
        time.sleep(0.05)
        for event in pygame.event.get():
            str(pygame.event.get())
            if event.type == wiiboard.WIIBOARD_MASS:
                if (event.mass.totalWeight > weight_threshold):
                    #time.sleep(0.05)
                    if recording:
                        maSurface = pygame.display.set_mode((500, 300))
                        maSurface.fill((255,255,255))
                        pygame.draw.line(maSurface, (0, 0, 0),
                                         (250, 0), (250, 300), 1)
                        pygame.draw.line(maSurface, (0, 0, 0),
                                         (0, 150), (500, 150), 1)
                        pygame.display.set_caption('Wiiboard caption')
                        total = event.mass.totalWeight
                        x = ((event.mass.topLeft + event.mass.bottomLeft)-(event.mass.topRight + event.mass.bottomRight) 
                             ) / total
                        y = ((event.mass.topRight + event.mass.topLeft) -
                             (event.mass.bottomRight + event.mass.bottomLeft)) / total
#                        output_filename = 'stab_' + time.asctime() + '.txt'
#                        output_file = open(output_filename, 'wt')
#                        output_file.write(`time.time() - init_time`+'\t')
#                        output_file.write(`event.mass.totalWeight`+'\t')
#                        output_file.write(`event.mass.topLeft`+'\t')
#                        output_file.write(`event.mass.topRight`+'\t')
#                        output_file.write(`event.mass.bottomLeft`+'\t')
#                        output_file.write(`event.mass.bottomRight`+'\t')
#                        output_file.write(`x`+'\t')
#                        output_file.write(`y`+'\n')
#                        output_file.flush()
                        x_1 = int(x*245)
                        y_1 = int(y*145)
#                        print (`x_1` +'\t' + `y_1` + '\n')
                        pygame.draw.rect(maSurface, (0, 0, 0), [
                                         (250 + x_1), (150 + y_1), 5, 5])
                        # pygame.event.clear()
                        pygame.display.update()
                        time.sleep(0.001)

                        # End of recording ?
                        if ((time.time() - init_time) > time_limit):
                            recording = False
                            print "End of recording"
#                            output_file.close()
#                            curses.beep()#

                  #  else:
                   #     pygame.event.clear()
            # The BUTTON event activates recording
            elif event.type == wiiboard.WIIBOARD_BUTTON_PRESS:
                print "Bouton devant"
                print "Button pressed!"

            elif event.type == wiiboard.WIIBOARD_BUTTON_RELEASE:
                if not recording:
                    print "Bouton inconnu"
                    print "Button released -> recording...."
#                    curses.beep()
#                    output_filename = 'stab_' + time.asctime() + '.txt'
#                    print "Save data in " + output_filename
#                    output_file = open(output_filename, 'wt')
#                    output_file.write(
#                        "Time\tWeight\tC_tl\tC_tr\tC_bl\tC_br\tX\tY\n")
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
