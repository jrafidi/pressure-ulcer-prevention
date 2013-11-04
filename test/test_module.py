from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import reactor

import time

SERVER_HOST = "localhost"
SERVER_PORT = 8123

class TestModule(Protocol):
  def connectionMade(self):
    self.sendMessage("Serial Number: 12345") # Fake serial number
    # time.sleep(1)

    # while 1:
    #   self.sendMessage("30")
    #   time.sleep(1)

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
  reactor.connectTCP(SERVER_HOST, SERVER_PORT, TestModuleFactory())
  reactor.run()