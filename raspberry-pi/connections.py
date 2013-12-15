from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.serialport import SerialPort
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import task
import main
import accel_processing as accel
import json
import time

class ModuleServerSocket(Protocol):
  def __init__(self, stateController):
    self.serverReady = False
    self.stateController = stateController

  def connectionMade(self):
    print 'successful connection to server'
    time.sleep(1)
    data = {
      'type': 'serial_number',
      'serial_number': main.MODULE_ID
    }

    # Have to use transport.write here due to server ready flag
    self.transport.write(json.dumps(data) + '\n')

  def dataReceived(self, line):
    if "OK" in line:
      self.serverReady = True
      return

    if "SETTING:" in line:
      bits = line.strip().split(":")
      if 'sleep' in bits[1].strip():
        self.stateController.sleepIntervalMs = int(bits[2].strip())
      elif 'sit' in bits[1].strip():
        self.stateController.sitIntervalMs = int(bits[2].strip())

  def sendMessage(self, message):
    if self.serverReady:
      self.transport.write(message + '\n')

class ModuleFactory(ReconnectingClientFactory):
  def __init__(self, stateController):
    self.connections = []
    self.stateController = stateController
  
  def logTurn(self, turnData):
    turnData['type'] = 'turn'
    self.broadcastMessage(json.dumps(turnData))

  def updateState(self, angle, sleeping):
    data = {
      'type': 'update',
      'angle': angle,
      'sleeping': sleeping
    }
    self.broadcastMessage(json.dumps(data))

  def debug(self, vals):
    data = {
      'type': 'debug',
      'vals': vals
    }
    self.broadcastMessage(json.dumps(data))

  def buildProtocol(self, addr):
    self.resetDelay()
    module = ModuleServerSocket(self.stateController)
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
    line = (self.lastData + data).strip()
    if len(line) == 0:
      self.lastData = line
      return

    if line[0] == '[' and line[len(line) - 1] == ']':
      line = line.replace('[', '').replace(']', '')
      vals = line.strip().split(',')
      self.lastData = ''
      angle = accel.calculateAngle(vals)
      sleeping = accel.calculateSleeping(vals)
      vectors = accel.getVectors(vals)
      self.stateController.updateState(angle, sleeping)
    else:
      bits = line.strip().split('[')
      self.lastData = '[' + bits[len(bits) - 1]
