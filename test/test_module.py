from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor, task

import time

SERVER_HOST = "localhost"
SERVER_PORT = 8123

class TestModule(Protocol):
  def connectionMade(self):
    self.sendMessage("Serial Number: 12345") # Fake serial number

  def sendData(self):
    self.sendMessage("30")

  def dataReceived(self, line):
    if line.strip() == "OK":
      self.lc = task.LoopingCall(self.sendData)
      self.lc.start(1)      

  def sendMessage(self, message):
    print message
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