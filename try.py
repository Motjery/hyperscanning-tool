#! /usr/bin/python
# coding : utf-8

# import stabilowii_raspberry
import pygame
import time
import numpy as np
import socket
import threading
import pygame.gfxdraw
from pygame.locals import *

host = '10.216.25.133'
port = 50000
port2 = 40000
port_start = 3000
port_search = 5000
port_filter = 10000
port_processing = 4000


class ThreadReception(threading.Thread):
    """objet thread gerant la reception des messages"""

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connection = conn           # ref. du socket de connection##

    def run(self):
        while 1:
            message_recu = self.connection.recv(256)
#            message_recu = message_recu.decode()
            a = message_recu.split("|")
            coordone = a[len(a) - 2]
            return(coordone)


pygame.init()


def main():

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    connection.bind((host,port))
    connection2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    pd_connection_start = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    pd_connection_search = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    pd_connection_filter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    pd_connection_processing = socket.socket(
#        socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection.connect((host, port))
        connection2.connect((host, port2))
#        pd_connection_start.connect((host, port_start))
#        pd_connection_search.connect((host, port_search))
#        pd_connection_filter.connect((host, port_filter))
#        pd_connection_processing.connect((host, port_processing))
    except socket.error:
        print ("La connection a echoue.")
        sys.exit()
    print ("connection etablie avec le serveur.")
    off = True
#    pd_connection_search.send("on;")
#    pd_connection_start.send("1;")
#    pd_connection_processing.send("ok;")

# initialization wiifit

    # pygame.draw.line(maSurface, (0, 0, 0),
    #                 (250, 0), (250, 300), 1)
    # pygame.draw.line(maSurface, (0, 0, 0),
    #                 (0, 150), (500, 150), 1)
#    maSurface.blit(bg, (0, 0))
#    bg = pygame.image.load("wiiboard.jpg")

#    pygame.display.set_caption('Wiiboard caption')

    while 1:
        maSurface = pygame.display.set_mode((710, 460))
        bg = pygame.image.load("wiiboard.jpg")
        maSurface.fill((255, 255, 255))
        maSurface = pygame.display.set_mode((710, 460))
        msg_rcv = ThreadReception(connection)
        msg_rcv1 = ThreadReception(connection2)
#        maSurface.fill((255, 255, 255))
#        pygame.draw.line(maSurface, (0, 0, 0),
#                         (250, 0), (250, 300), 1)
#        pygame.draw.line(maSurface, (0, 0, 0),
#                         (0, 150), (500, 150), 1)
        maSurface.blit(bg, (0, 0))
        pygame.display.set_caption('Wiiboard caption')

        try:
            reception_board2 = msg_rcv.run()
            a = reception_board2.split(",")
            y2 = float(a[len(a) - 2])
            x2 = float(a[0])
            x_2 = int(x2 * 345)
            y_2 = - int(y2 * 217)
        except:
            pass
        try:
            reception_board1 = msg_rcv1.run()
            a = reception_board1.split(",")
            y1 = float(a[len(a) - 2])
            x1 = float(a[0])
            x_1 = int(x1 * 345)
            y_1 = - int(y1 * 217)
        except:
            pass
        try:
            pygame.draw.rect(maSurface, (255, 0, 0), [
                (357 + int(x_2)), (230 + int(y_2)), 10, 10])
            pygame.draw.rect(maSurface, (255, 255, 0), [
                (357 + int(x_1)), (230 + int(y_1)), 10, 10])
            pygame.display.update()
        except:
            pass
#        if off is True:
#            try:
#                if x_2 in xrange(x_1 - 50, x_1 + 50):
#                    if y_2 in xrange(y_1 - 50, y_1 + 50):
#                        pd_connection_filter.send("120;")
#                        pd_connection_filter.send("0;")
#                elif x_2 in xrange(x_1 - 60, x_1 + 60):
#                    if y_2 in xrange(y_1 - 60, y_1 + 60):
#                        pd_connection_filter.send("110;")
#                        pd_connection_filter.send("1;")
#                elif x_2 in xrange(x_1 - 70, x_1 + 70):
#                    if y_2 in xrange(y_1 - 70, y_1 + 70):
#                        pd_connection_filter.send("100;")
#                        pd_connection_filter.send("1;")
#                elif x_2 in xrange(x_1 - 80, x_1 + 80):
#                    if y_2 in xrange(y_1 - 80, y_1 + 80):
#                        pd_connection_filter.send("90;")
#                        pd_connection_filter.send("2;")
#                elif x_2 in xrange(x_1 - 90, x_1 + 90):
#                    if y_2 in xrange(y_1 - 90, y_1 + 90):
#                        pd_connection_filter.send("80;")
#                        pd_connection_filter.send("2;")
#                elif x_2 in xrange(x_1 - 100, x_1 + 100):
#                    if y_2 in xrange(y_1 - 100, y_1 + 100):
#                        pd_connection_filter.send("70;")
#                        pd_connection_filter.send("2;")
#                elif x_2 in xrange(x_1 - 120, x_1 + 120):
#                    if y_2 in xrange(y_1 - 120, y_1 + 120):
#                        pd_connection_filter.send("60;")
#                        pd_connection_filter.send("3;")
#                else:
#                    pd_connection_filter.send("50;")
#                    pd_connection_filter.send("3;")
#            except:
#               pass
    if pygame.event == pygame.quit():
        0
        pygame.quit()
#        pd.pd_connection_start.send("0;")
        off = True


if __name__ == "__main__":
    main()
