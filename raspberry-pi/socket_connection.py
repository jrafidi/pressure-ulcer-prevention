from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor, task

class Module(Protocol):
  def connectionMade(self):
    self.sendMessage("Serial Number: " + str(MODULE_ID))

  def dataReceived(self, line):
    if "SETTING" in line:
      bits = line.strip().split(":")
      print bits[1].strip() + " set to " + bits[2].strip()   

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class ModuleFactory(ReconnectingClientFactory):
  def __init__(self):
    self.connections = []
  
  def buildProtocol(self, addr):
    self.resetDelay()
    module = Module()
    self.connections.append(module)
    return module

  def broadcastMessage(self, msg):
    for conn in self.connections:
      conn.sendMessage(msg)

  def clientConnectionLost(self, connector, reason):
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                     reason)
