from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.serialport import SerialPort
from twisted.internet import reactor

from connections import *
from state import *

SERVER_HOST = '275pup.xvm.mit.edu'
SERVER_PORT = 7123
MODULE_ID = 1

SERIAL_PORT_0 = '/dev/ttyACM0'
SERIAL_PORT_1 = '/dev/ttyACM1'
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
    try:
        SerialPort(serialClient, SERIAL_PORT_0, reactor, baudrate=SERIAL_BAUD)
    except OSError:
        SerialPort(serialClient, SERIAL_PORT_1, reactor, baudrate=SERIAL_BAUD)
    reactor.run()
