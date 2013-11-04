from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import reactor

TEST_DATA = []

SERVER_HOST = "localhost"
SERVER_PORT = 8123

class TestModule(Protocol):
  def connectionMade(self):
    # TODO: start sending a bunch of dummy data across the wire
    self.transport.write("12345") # Fake serial number

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