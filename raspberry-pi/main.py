from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.serialport import SerialPort
from twisted.internet import reactor

from connections import *
from state import *

SERVER_HOST = '18.238.6.222'
SERVER_PORT = 7123
MODULE_ID = 1

# TODO: smartly find this port
SERIAL_PORT = '/dev/ttyACM1'
SERIAL_BAUD = '9600'

if __name__ == '__main__':
    stateController = ModuleStateController()
    socketFactory = ModuleFactory(stateController)
    serialClient = SerialClient(stateController)

    # Hacky to have model and socket pointed at each other.
    # Better done using Model and triggering, but lazy right now.
    stateController.setSocketFactory(socketFactory)

    point = TCP4ClientEndpoint(reactor, SERVER_HOST, SERVER_PORT)
    d = point.connect(socketFactory)
    SerialPort(serialClient, SERIAL_PORT, reactor, baudrate=SERIAL_BAUD)
    reactor.run()
