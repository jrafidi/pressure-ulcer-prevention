from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor, task

import time
from random import randint

SERVER_HOST = "localhost"
SERVER_PORT = 8123
DATA_CENTER = 30

MODULE_ID = randint(0, 10000)

class TestModule(Protocol):
  def connectionMade(self):
    self.sendMessage("Serial Number: " + str(MODULE_ID))

  def sendData(self):
    data = DATA_CENTER + randint(0, 100) * 0.01 - 0.5
    self.sendMessage(str(data))

  def dataReceived(self, line):
    if line.strip() == "OK":
      self.lc = task.LoopingCall(self.sendData)
      self.lc.start(1)

    if "SETTING" in line:
      bits = line.strip().split(":")
      print bits[1].strip() + " set to " + bits[2].strip()   

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