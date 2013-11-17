from twisted.internet.serialport import SerialPort
from twisted.internet.protocol import Protocol, Factory

import accel_processing as accel

class SerialClient(Protocol):
    def __init__(self, socketFactory):
        self.socketFactory = socketFactory
        self.lastData = ''

    def dataReceived(self, data):
        line = self.lastData + data

        if len(line.strip()) != 23:
            self.lastData = line
        else:
            vals = line.strip().split(' ')
            self.lastData = ''
            print str(vals)
            print accel.calculateAngle(vals)
