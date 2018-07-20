# coding: utf-8

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import socket
import sys
import threading
import numpy as np
from scipy import signal, stats

host = '10.216.25.133'
host2 = '10.216.37.28'
port = 50000
port2 = 40000
port_filter = 10000
timer = {}


class ThreadReception(threading.Thread):
    """objet thread gerant la reception des messages"""

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connection = conn
        # ref. du socket de connection###

    def run(self):
        while 1:
            message_recu = self.connection.recv(1024)
            message_recu = message_recu.decode()
            a = message_recu.split("|")
            coordone = a[len(a) - 2]
            return(coordone)


def resizing(tab, size):
    if(len(tab) > size):
        tab = tab[1:len(tab):1]
        return tab
    else:
        return tab
#        print(len(tab))


def crosscorr(a, b):
    np.seterr(divide='ignore', invalid='ignore')
    try:
        a = (a - np.mean(a)) / (np.std(a) * len(a))
        b = (b - np.mean(b)) / (np.std(b))
        cross_corre = signal.fftconvolve(a, b[::-1], mode='same')
        return cross_corre
    except:
        pass


def coefcross(a, b):
    np.seterr(divide='ignore', invalid='ignore')
    try:
        coef_corre = stats.pearsonr(a, b)
        return coef_corre[0]
    except:
        pass


def compare(coef_pearsona, coef_pearsonb):

    coef_pearsonX = np.abs(coef_pearsona)
    coef_pearsonY = np.abs(coef_pearsonb)
    coef_pearson = (coef_pearsonY + coef_pearsonX) / 2
    values = np.arange(0, 1, 0.1)
    message = np.arange(10, 20, 1)
    i = 9
    while i >= 0:
        if coef_pearson < values[i]:
            i -= 1
        else:
            a = str(message[i]) + ";"
            print(a)
#            pd_connection_filter.send((a).encode())
            i = -1


def makegrahupdate(graph, number):
    global timer
    timer['time' + str(number)] = QtCore.QTimer()
    timer['time' + str(number)].timeout.connect(graph)
    timer['time' + str(number)].start()


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#pd_connection_filter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connection.close()
#connection.bind((host, port))

connection.connect((host, port))
connection2.connect((host, port2))
#pd_connection_filter.connect((host2, port_filter))

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('Plots stabilometric')
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


# X borad 1
p1 = win.addPlot(title="Board 1 : X")
p1.setYRange(-1.5, 1.5)
x1 = np.array([])
t1 = np.array([])
curve1 = p1.plot(pen='y')


def update1():
    global curve1, x1, t1, p1
    msg_rcv = ThreadReception(connection2)
    try:
        reception_board2 = msg_rcv.run()
    #    data , addr = connection.recvfrom(256)
    #    data = data.decode()
        b = reception_board2.split(",")
        t_1 = float(b[2])
        t1 = np.append(t1, t_1)
        t1 = resizing(t1, 30)
        x_1 = float(b[0])
        x1 = np.append(x1, x_1)
        x1 = resizing(x1, 30)
        curve1.setData(t1, x1)
    except:
        #curve1.setData(t1, x1)
        pass



# Y borad 1
p2 = win.addPlot(title="Board 1 : Y")
p2.setYRange(-1.5, 1.5)
y1 = np.array([])
t12 = np.array([])
curve2 = p2.plot(pen='y')


def update2():
    global curve2, y1, t12, p2
    msg_rcv = ThreadReception(connection2)
    try:
        reception_board2 = msg_rcv.run()
    #    data, addr = connection.recvfrom(256)
        b = reception_board2.split(",")
        t_12 = float(b[2])
        t12 = np.append(t12, t_12)
        t12 = resizing(t12, 30)
        y_1 = float(b[1])
        y1 = np.append(y1, y_1)
        y1 = resizing(y1, 30)
        curve2.setData(t12, y1)
    except:
        #curve2.setData(t12, y1)
        pass


p5 = win.addPlot(title="Stabilometry Board 1")
p5.setYRange(-1, 1)
p5.setXRange(-1, 1)

x3 = np.array([])
y3 = np.array([])
curve5 = p5.plot(pen='y')


def update5():
    global curve5, x3, y3, p5
    msg_rcv = ThreadReception(connection2)
    try:
        reception_board2 = msg_rcv.run()
    #    data , addr = connection.recvfrom(256)
    #    data = data.decode()
        b = reception_board2.split(",")
        y_3 = float(b[1])
        y3 = np.append(y3, y_3)
        y3 = resizing(y3, 60)
        x_3 = float(b[0])
        x3 = np.append(x3, x_3)
        x3 = resizing(x3, 60)
        curve5.setData(x3, y3)
    except:
        #curve1.setData(t1, x1)
        pass


win.nextRow()


# X borad 2
p3 = win.addPlot(title="Board 2 : X")
p3.setYRange(-1.5, 1.5)
x2 = np.array([])
t2 = np.array([])
curve3 = p3.plot(pen='r')


def update3():
    global curve3, x2, t2, p3
    msg_rcv = ThreadReception(connection)
    try:
        reception_board2 = msg_rcv.run()
        b = reception_board2.split(",")
        t_2 = float(b[2])
        t2 = np.append(t2, t_2)
        t2 = resizing(t2, 30)
        x_2 = float(b[0])
        x2 = np.append(x2, x_2)
        x2 = resizing(x2, 30)
        curve3.setData(t2, x2)
    except:
        #curve3.setData(t2, x2)
        pass


# Y borad 2#

p4 = win.addPlot(title="Borad 2 : Y")
p4.setYRange(-1.5, 1.5)
y2 = np.array([])
t22 = np.array([])
curve4 = p4.plot(pen='r')


def update4():
    global curve4, y2, t22, p4
    msg_rcv = ThreadReception(connection)
    try:
        reception_board2 = msg_rcv.run()
    #    data, addr = connection.recvfrom(256)
        b = reception_board2.split(",")
        t_22 = float(b[2])
        t22 = np.append(t22, t_22)
        t22 = resizing(t22, 30)
        y_2 = float(b[1])
        y2 = np.append(y2, y_2)
        y2 = resizing(y2, 30)
        curve4.setData(t22, y2)
    except:
        #curve2.setData(t12, y1)
        pass


p6 = win.addPlot(title="Stabilometry Board 2")
p6.setYRange(-1, 1)

p6.setXRange(-1, 1)
x4 = np.array([])
y4 = np.array([])
curve6 = p6.plot(pen='r')


def update6():
    global curve6, x4, y4, p6
    msg_rcv = ThreadReception(connection)
    try:
        reception_board2 = msg_rcv.run()
    #    data , addr = connection.recvfrom(256)
    #    data = data.decode()
        b = reception_board2.split(",")
        y_4 = float(b[1])
        y4 = np.append(y4, y_4)
        y4 = resizing(y4, 60)
        x_4 = float(b[0])
        x4 = np.append(x4, x_4)
        x4 = resizing(x4, 60)
        curve6.setData(x4, y4)
    except:
        #curve1.setData(t1, x1)
        pass


win.nextRow()


p7 = win.addPlot(title="Cross correlation X")
p7.setYRange(-1, 1)
curve7 = p7.plot(pen='c')

coeffX = 0.0


def update7():
    global crossX, coeffX, p7, curve7
    try:
        crossX = crosscorr(x1, x2)
        samplesX = np.arange(len(crossX))
        coeffX = coefcross(x1, x2)
        curve7.setData(samplesX, crossX)
        return coeffX
    except:
        pass


p8 = win.addPlot(title="Cross correlation Y")
p8.setYRange(-1, 1)
curve8 = p8.plot(pen='c')

global coeffY


def update8():
    global curve8, crossY, coeffY
    try:

        crossY = crosscorr(y1, y2)
        samplesY = np.arange(len(crossY))
        coeffY = coefcross(y1, y2)
        compare(coeffX, coeffY)
        curve8.setData(samplesY, crossY)
    except:
        pass


makegrahupdate(update1, 1)
makegrahupdate(update2, 2)
makegrahupdate(update3, 3)
makegrahupdate(update4, 4)
makegrahupdate(update5, 5)
makegrahupdate(update6, 6)
makegrahupdate(update7, 7)
makegrahupdate(update8, 8)

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
