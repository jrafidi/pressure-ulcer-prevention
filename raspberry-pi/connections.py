from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.serialport import SerialPort
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import task
import accel_processing as accel
import json

class ModuleServerSocket(Protocol):
  def __init__(self):
    self.serverReady = False

  def connectionMade(self):
    self.sendMessage("SERIAL_NUMBER:" + str(MODULE_ID))

  def dataReceived(self, line):
    if "OK" in line:
      self.serverReady = True
      return

    if "ALL_SETTINGS:" in line:
      # TODO: update state with all settings

    if "SETTING:" in line:
      bits = line.strip().split(":")
      print bits[1].strip() + " set to " + bits[2].strip()
      # TODO: update state

  def sendMessage(self, message):
    if self.serverReady:
      self.transport.write(message + '\n')

class ModuleFactory(ReconnectingClientFactory):
  def __init__(self, stateController):
    self.connections = []
    self.stateController = stateController
  
  def logTurn(self, turnData):
    self.broadcastMessage("TURN:" + json.dumps(turnData))

  def updateAngle(self, angle):
    self.broadcastMessage("ANGLE:" + str(angle))

  def buildProtocol(self, addr):
    self.resetDelay()
    module = ModuleServerSocket()
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


class SerialClient(Protocol):
  def __init__(self, stateController):
    self.stateController = stateController

    self.lastData = ''

  def dataReceived(self, data):
    # Hacky hack hack
    line = self.lastData + data
    if len(line.strip()) != 23:
      self.lastData = line
    else:
      vals = line.strip().split(' ')
      self.lastData = ''
      angle = accel.calculateAngle(vals)
      sleeping = accel.calculateSleeping(vals)
      self.stateController.updateState(angle, sleeping)