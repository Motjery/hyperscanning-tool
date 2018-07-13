# coding: utf-8

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import socket
import sys
import threading

host = '10.216.25.133'
port = 50000
port2 = 40000


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




connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connection.close()
#connection.bind((host, port))

connection.connect((host, port))
connection2.connect((host, port2))


app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('Plots stabilometric')
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


# X borad 1
p1 = win.addPlot(title="Board 1 : X")
p1.setYRange(-1.5, 1.5)
x1 = []
t1 = []
curve1 = p1.plot(pen='y')

def update1():
    global curve1, x1, t1, p1
    msg_rcv = ThreadReception(connection2)
    try:
        reception_board2 = msg_rcv.run()
        print(reception_board2)
    #    data , addr = connection.recvfrom(256)
    #    data = data.decode()
        b = reception_board2.split(",")
        t_1 = float(b[2])
        t1.append(t_1)
        x_1 = float(b[0])
        x1.append(x_1)
        curve1.setData(t1, x1)
    except:
        #curve1.setData(t1, x1)
        pass



# Y borad 1
p2 = win.addPlot(title="Board 1 : Y")
p2.setYRange(-1.5, 1.5)
y1 = []
t12 = []
curve2 = p2.plot(pen='y')

def update2():
    global curve2, y1, t12, p2
    msg_rcv = ThreadReception(connection2)
    try:
        reception_board2 = msg_rcv.run()
    #    data, addr = connection.recvfrom(256)
        b = reception_board2.split(",")
        t_12 = float(b[2])
        t12.append(t_12)
        y_1 = float(b[1])
        y1.append(y_1)
        curve2.setData(t12, y1)
    except:
        #curve2.setData(t12, y1)
        pass


p5 = win.addPlot(title="Borad 1 : XY")
x3 = []
y3 = []
curve5 = p5.plot(pen='y')

def update5():
    global curve5, x3, y3, p5
    msg_rcv = ThreadReception(connection2)
    try:
        reception_board2 = msg_rcv.run()
        print(reception_board2)
    #    data , addr = connection.recvfrom(256)
    #    data = data.decode()
        b = reception_board2.split(",")
        y_3 = float(b[1])
        y3.append(y_3)
        x_3 = float(b[0])
        x3.append(x_3)
        curve5.setData(x3, y3)
    except:
        #curve1.setData(t1, x1)
        pass

win.nextRow()


# X borad 2
p3 = win.addPlot(title="Board 2 : X")
p3.setYRange(-1.5, 1.5)
x2 = []
t2 = []
curve3 = p3.plot(pen='r')

def update3():
    global curve3, x2, t2, p3
    msg_rcv = ThreadReception(connection)
    try:
        reception_board2 = msg_rcv.run()
        b = reception_board2.split(",")
        t_2 = float(b[2])
        t2.append(t_2)
        x_2 = float(b[0])
        x2.append(x_2)
        curve3.setData(t2, x2)
    except:
        #curve3.setData(t2, x2)
        pass


# Y borad 2#

p4 = win.addPlot(title="Borad 2 : Y")
p4.setYRange(-1.5, 1.5)
y2 = []
t22 = []
curve4 = p4.plot(pen='r')

def update4():
    global curve4, y2, t22, p4
    msg_rcv = ThreadReception(connection)
    try:
        reception_board2 = msg_rcv.run()
        b = reception_board2.split(",")
        t_22 = float(b[2])
        t22.append(t_22)
        y_2 = float(b[1])
        y2.append(y_2)
        curve4.setData(t22, y2)
    except:
        #curve4.setData(t22, y2)
        pass

p6 = win.addPlot(title="Borad 1 : XY")
x4 = []
y4 = []
curve6 = p6.plot(pen='r')

def update6():
    global curve6, x4, y4, p6
    msg_rcv = ThreadReception(connection)
    try:
        reception_board2 = msg_rcv.run()
        print(reception_board2)
    #    data , addr = connection.recvfrom(256)
    #    data = data.decode()
        b = reception_board2.split(",")
        y_4 = float(b[1])
        y4.append(y_4)
        x_4 = float(b[0])
        x4.append(x_4)
        curve6.setData(x4, y4)
    except:
        #curve1.setData(t1, x1)
        pass



timer = QtCore.QTimer()
timer.timeout.connect(update1)
timer.start()

timer2 = QtCore.QTimer()
timer2.timeout.connect(update2)
timer2.start()

timer3 = QtCore.QTimer()
timer3.timeout.connect(update3)
timer3.start()    #

timer4 = QtCore.QTimer()
timer4.timeout.connect(update4)
timer4.start()

timer5 = QtCore.QTimer()
timer5.timeout.connect(update5)
timer5.start()

timer6 = QtCore.QTimer()
timer6.timeout.connect(update6)
timer6.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

