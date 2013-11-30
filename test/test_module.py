from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor, task

import time
import json
from random import randint

SERVER_HOST = "localhost"
SERVER_PORT = 7123
DATA_CENTER = randint(-30, 30)

MODULE_ID = randint(0, 10000)

class TestModule(Protocol):
  def connectionMade(self):
    print 'successful connection to server'
    time.sleep(1)
    data = {
      'type': 'serial_number',
      'serial_number': MODULE_ID
    }
    self.sendMessage(json.dumps(data))

  def sendData(self):
    angle = DATA_CENTER + randint(-250, 250) * 0.01
    sleeping = True
    data = {
      'type': 'update',
      'angle': angle,
      'sleeping': sleeping
    }
    self.sendMessage(json.dumps(data))

  def dataReceived(self, line):
    if line.strip() == "OK":
      self.lc = task.LoopingCall(self.sendData)
      self.lc.start(1)

    if "SETTING:" in line:
      print line

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class TestModuleFactory(ReconnectingClientFactory):
  def buildProtocol(self, addr):
    self.resetDelay()
    return TestModule()

  def clientConnectionLost(self, connector, reason):
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                     reason)

if __name__ == '__main__':
  point = TCP4ClientEndpoint(reactor, SERVER_HOST, SERVER_PORT)
  d = point.connect(TestModuleFactory())
  reactor.run()