from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import reactor

import time

SERVER_HOST = "localhost"
SERVER_PORT = 8123

class TestModule(Protocol):
  def connectionMade(self):
    self.transport.write("Serial Number: 12345\n") # Fake serial number

    while 1:
      self.transport.write("30\n")
      time.sleep(1)

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