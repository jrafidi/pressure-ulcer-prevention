from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

from ..model.ModuleModel import ModuleModel

import json

class PatientModuleReceiver(LineReceiver):
  def __init__(self, session):
    self.session = session

  def registerModule(self, id):
    self.id = id
    self.model = ModuleModel(id)
    self.session.addModule(self.model)

    self.model.on("change:sleep_interval_ms", self.updateState)
    self.model.on("change:sit_interval_ms", self.updateState)

    # TODO: look in DB for previous settings for this module and set

    # Tell module to start sending data
    self.sendMessage("OK")

  def updateState(self, model, attr):
    self.sendMessage("SETTING: " + attr + ":" + model.get(attr))

  def connectionLost(self, reason):
    self.session.removeModule(self.id)

  def dataReceived(self, line):
    lines = line.strip().split('\n')
    for l in lines:
      data = json.loads(l)
      if data['type'] == 'serial_number':
        self.registerModule(data['serial_number'])
      elif data['type'] == 'update':
        self.model.set('angle', data['angle'])
        self.model.set('sleeping', data['sleeping'])
      elif data['type'] == 'turn':
        turns = self.model.get('turns')
        turns.append(data)
        self.model.set('turns', turns)

  def sendMessage(self, message):
    self.transport.write(message + '\n')


class PatientModuleSocketFactory(Factory):
  def __init__(self, session):
    self.session = session

  def buildProtocol(self, addr):
    return PatientModuleReceiver(self.session)