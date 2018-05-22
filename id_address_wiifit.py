#! /usr/bin/python3

import bluetooth as ble
import time
import sys
import codecs
import collections


# --------- User Settings ---------
WEIGHT_SAMPLES = 500
# ---------------------------------

target_name = "Nintendo RVL-WBC-01"
# Wiiboard Parameters
CONTINUOUS_REPORTING = "04"  # Easier as string with leading zero
COMMAND_LIGHT = 11
COMMAND_REPORTING = 12
COMMAND_REQUEST_STATUS = 15
COMMAND_REGISTER = 16
COMMAND_READ_REGISTER = 17
INPUT_STATUS = 20
INPUT_READ_DATA = 21
EXTENSION_8BYTES = 32
BUTTON_DOWN_MASK = 8
TOP_RIGHT = 0
BOTTOM_RIGHT = 1
TOP_LEFT = 2
BOTTOM_LEFT = 3


class EventProcessor:
    def __init__(self):
        self._measured = False
        self.done = False
        self._measureCnt = 0
        self._events = list(range(WEIGHT_SAMPLES))

    def mass(self, event):
        if (event.totalWeight > 2):
            self._events[self._measureCnt] = event.totalWeight * 2.20462
            self._measureCnt += 1
            if self._measureCnt == WEIGHT_SAMPLES:
                self._sum = 0
                for x in range(0, WEIGHT_SAMPLES - 1):
                    self._sum += self._events[x]
                self._weight = self._sum / WEIGHT_SAMPLES
                self._measureCnt = 0
                print((self._weight, " lbs"))
            if not self._measured:
                self._measured = True

    @property
    def weight(self):
        if not self._events:
            return 0
        histogram = collections.Counter(round(num, 1) for num in self._events)
        return histogram.most_common(1)[0][0]


class BoardEvent():
    def __init__(self, topLeft, topRight, bottomLeft, bottomRight, buttonPressed, buttonReleased):

        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.buttonPressed = buttonPressed
        self.buttonReleased = buttonReleased
        # convenience value
        self.totalWeight = topLeft + topRight + bottomLeft + bottomRight


class Wii():
    """docstring forWii"""

    def __init__(self, processor):
        # Sockets and status
        self.receivesocket = None
        self.controlsocket = None

        self.processor = processor
        self.calibration = []
        self.calibrationRequested = False
        self.led = False
        self.target_address = None
        self.buttonDown = False
        for i in range(3):
            self.calibration.append([])
            for j in range(4):
                # high dummy value so events with it don't register
                self.calibration[i].append(10000)

        self.status = "Disconnected"
        self.lastEvent = BoardEvent(0, 0, 0, 0, False, False)

        try:
            self.receivesocket = ble.BluetoothSocket(ble.L2CAP)
            self.controlsocket = ble.BluetoothSocket(ble.L2CAP)
        except ValueError:
            raise Exception("Error: Bluetooth not found")

    def searchwi(self):
        target_address = None
        print("Press the red sync button")
        near_devices = ble.discover_devices(duration=5)

        for bdaddr in near_devices:
            if target_name == ble.lookup_name(bdaddr):
                target_address = bdaddr
                break

        if target_address is not None:
            print("Wii fit address is:", target_address)
        else:
            print("No wii fit found")
            sys.exit()

        return target_address

    def connection(self, target_address):
        if target_address is None:
            print("Non existant address")
            return
        self.receivesocket.connect((target_address, 0x13))
        self.controlsocket.connect((target_address, 0x11))
        if self.receivesocket and self.controlsocket:
            print("Connected to Wii fit at address ", target_address)
            self.status = "Connected"
            self.target_address = target_address
            self.setReportingType()
            useExt = ["00", COMMAND_REGISTER, "04", "A4", "00", "40", "00"]
            self.send(useExt)
            self.setReportingType()
            print ("Wiiboard connected")
        else:
            print ("Could not connect to Wii fit: ", target_address)

    def disconnect(self):
        if self.status == "Connected":
            #            self.status = "Disconnecting"
            #            while self.status == "Disconnecting":
            #                self.wait(50)
            #        try:
            #            print("p1")
            self.receivesocket = self.receivesocket.close()
#        except:
#            pass
#        try:
            self.controlsocket = self.controlsocket.close()
#        except:
#            pass
            self.status = "Disconnected"
            print(f'WiiBoard {self.status}')
        else:
            print ("WiiBoard not connected")

    def send(self, data):
        if self.status != "Connected":
            return
        data[0] = "52"

        senddata = ""
        for bytes in data:
            # bytes = str(bytes)
            senddata += b'data[bytes]'.hex()
        senddata = b'senddata'
        self.controlsocket.send(senddata)
# à faire dans un autre fichier

    def receive(self):
        while self.status == "Connected":  # and not self.processor.done:
            data = self.receivesocket.recv(25)
            intype = int(data.hex()[2:4], 16)
            print(intype, " stat ", INPUT_STATUS, " read", INPUT_READ_DATA)
            if intype == INPUT_STATUS:
                # TODO: Status input received. It just tells us battery life really
                self.setReportingType()
            elif intype == INPUT_READ_DATA:
                if self.calibrationRequested:
                    packetLength = (data[4].hex() / 16 + 1)
                    self.parseCalibrationResponse(data[7:(7 + packetLength)])

                    if packetLength < 16:
                        self.calibrationRequested = False
            elif intype == EXTENSION_8BYTES:
                self.processor.mass(self.createBoardEvent(data[2:12]))
            else:
                print("ACK to data write received")

    def createBoardEvent(self, bytes):
        buttonBytes = bytes[0:2]
        bytes = bytes[2:12]
        buttonPressed = False
        buttonReleased = False

        state = (int(buttonBytes.hex()[0], 16) << 8) | int(
            buttonBytes.hex()[1], 16)
        if state == BUTTON_DOWN_MASK:
            buttonPressed = True
            if not self.buttonDown:
                print("Button pressed")
                self.buttonDown = True

        if not buttonPressed:
            if self.lastEvent.buttonPressed:
                buttonReleased = True
                self.buttonDown = False
                print("Button released")

        rawTR = (int(bytes.hex()[0], 16) << 8) + int(bytes.hex()[1], 16)
        rawBR = (int(bytes.hex()[2], 16) << 8) + int(bytes.hex()[3], 16)
        rawTL = (int(bytes.hex()[4], 16) << 8) + int(bytes.hex()[5], 16)
        rawBL = (int(bytes.hex()[6], 16) << 8) + int(bytes.hex()[7], 16)

        topLeft = self.calcMass(rawTL, TOP_LEFT)
        topRight = self.calcMass(rawTR, TOP_RIGHT)
        bottomLeft = self.calcMass(rawBL, BOTTOM_LEFT)
        bottomRight = self.calcMass(rawBR, BOTTOM_RIGHT)
        boardEvent = BoardEvent(
            topLeft, topRight, bottomLeft,
            bottomRight, buttonPressed, buttonReleased)
        return boardEvent

    def calcMass(self, raw, pos):
        val = 0.0
#        calibration[0] is calibration values for 0kg
#        calibration[1] is calibration values for 17kg
#        calibration[2] is calibration values for 34kg
        print("raw", raw)
        print("calib", self.calibration[0][pos])
        if raw < self.calibration[0][pos]:
            return val
        elif raw < self.calibration[1][pos]:
            val = 17 * ((raw - self.calibration[0][pos]) / float(
                (self.calibration[1][pos] - self.calibration[0][pos])))
        elif raw > self.calibration[1][pos]:
            val = 17 + 17 * ((raw - self.calibration[1][pos]) / float(
                (self.calibration[2][pos] - self.calibration[1][pos])))

        return val

    def parseCalibrationResponse(self, bytes):
        index = 0
        if len(bytes) == 16:
            for i in range(2):
                for j in range(4):
                    self.calibration[i][j] = (
                        int(bytes.hex()[index], 16) << 8) + int(
                        bytes.hex()[index + 1], 16)
                    index += 2
        elif len(bytes) < 16:
            for i in range(4):
                self.calibration[2][i] = (
                    int(bytes.hex()[index], 16) << 8) + int(
                    bytes.hex()[index + 1], 16)
                index += 2

    def calibrate(self):
        message = ["00", COMMAND_READ_REGISTER,
                   "04", "A4", "00", "24", "00", "18"]
        self.send(message)
        self.calibrationRequested = True

    def setReportingType(self):
        bytearr = ["00", COMMAND_REPORTING,
                   CONTINUOUS_REPORTING, EXTENSION_8BYTES]
        self.send(bytearr)

    def isConnected(self):
        return self.status == "Connected"

    def wait(self, millis):
        time.sleep(millis / 1000.0)

    def getled(self):
        return self.led

    def setLight(self, light):
        if light:
            val = "10"
        else:
            val = "00"
        message = ["00", COMMAND_LIGHT, val]
        self.send(message)
        self.led = light


def main():

    processor = EventProcessor()
    board = Wii(processor)
#    if len(sys.argv) == 2:
#        print("Discovering board...")
#        target_address = board.discover()
#    else:
#        target_address = sys.argv[1]#

#    try:
#        # Disconnect already-connected devices.
#        # This is basically Linux black magic just to get the thing to work.
#        subprocess.check_output(["bluez-test-input", "disconnect", target_address], stderr=subprocess.STDOUT)
#        subprocess.check_output(["bluez-test-input", "disconnect", target_address], stderr=subprocess.STDOUT)
#    except:
#       pass
    print("Discovering board...")
    target_address = board.searchwi()

    board.connection(target_address)
    board.wait(200)
    board.setLight(False)
    board.wait(500)
    board.setLight(True)
    board.wait(500)
    board.receive()
#    board.disconnect()


if __name__ == "__main__":
    main()
