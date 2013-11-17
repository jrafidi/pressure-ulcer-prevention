from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.serialport import SerialPort
from twisted.internet import reactor

from socket_connection import *
from serial_connection import *

SERVER_HOST = 'localhost'
SERVER_PORT = 7123
MODULE_ID = 1

# TODO: smartly find this port
SERIAL_PORT = '/dev/ttyACM1'
SERIAL_BAUD = '9600'

if __name__ == '__main__':
    socketFactory = ModuleFactory()
    serialClient = SerialClient(socketFactory)

    point = TCP4ClientEndpoint(reactor, SERVER_HOST, SERVER_PORT)
    d = point.connect(socketFactory)
    SerialPort(serialClient, SERIAL_PORT, reactor, baudrate=SERIAL_BAUD)
    reactor.run()
