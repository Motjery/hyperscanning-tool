#! /usr/bin/python3

import bluetooth as ble
import time
import sys

target_name = "Nintendo RVL-WBC-01"
# target_address = None


class Wii(object):
    """docstring forWii"""

    def __init__(self):
                    # Sockets and status
        self.receivesocket = None
        self.controlsocket = None
        self.target_address = None
        self.status = "Disconnected"
        self.led = False
#        self.lastEvent = BoardEvent(0, 0, 0, 0, False, False)

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
            # break

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
            print ("Wiiboard connected")
        else:
            print ("Could not connect to Wii fit: ", target_address)

    def wait(self, millis):
        time.sleep(millis / 1000.0)

    def disconnect(self):
        if self.status == "Connected":
            self.status = "Disconnecting"
            while self.status == "Disconnecting":
                self.wait(100)
        try:
            self.receivesocket.close()
        except:
            pass
        try:
            self.controlsocket.close()
        except:
            pass
        print("WiiBoard disconnected")


def main():

    board = Wii()
    print("Discovering board...")
    target_address = board.searchwi()

    board.connection(target_address)
    board.wait(300)
#    board.setLight(True)
#    board.wait(200)
#    board.disconnect()


if __name__ == "__main__":
    main()
