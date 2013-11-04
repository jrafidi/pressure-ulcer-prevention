from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

from ..model.ModuleModel import ModuleModel

class PatientModuleReceiver(LineReceiver):
  def __init__(self, session):
    self.session = session

  def registerModule(self, id):
    self.id = id
    self.model = ModuleModel(id)
    self.session.moduleModels[id] = self.model

    print id

    # TODO: bind model listeners

  def updateState(self, model, attr):
    # TODO: update the timing setting for this module
    pass

  def connectionLost(self, reason):
    # TODO: update the session to note this module's disconnection
    pass

  def dataReceived(self, line):
    if "Serial Number" in line:
      self.registerModule(line.split(':')[1].strip())

    # TODO: update model based on new data

  def sendMessage(self, message):
    self.transport.write(message + '\n')


class PatientModuleSocketFactory(Factory):
  def __init__(self, session):
    self.session = session

  def buildProtocol(self, addr):
    return PatientModuleReceiver(self.session)