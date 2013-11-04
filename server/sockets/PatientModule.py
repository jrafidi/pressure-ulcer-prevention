from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class PatientModuleReceiver(LineReceiver):
  def __init__(self, session):
    self.session = session

  def updateState(self, model, attr):
    # TODO: update the timing setting for this module
    pass

  def connectionMade(self):
    # TODO: update the session to account for this module
    pass

  def connectionLost(self, reason):
    # TODO: update the session to note this module's disconnection
    pass

  def lineReceived(self, line):
    # TODO: update ready state to True based on line
    pass

  def sendMessage(self, message):
    self.transport.write(message + '\n')


class PatientModuleSocketFactory(Factory):
  def __init__(self, session):
    self.session = session

  def buildProtocol(self, addr):
    return PatientModuleReceiver(self.session)