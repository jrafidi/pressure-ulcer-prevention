from autobahn.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

import json

class PatientControlProtocol(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)
    self.sendMessage(self.factory.getState())

  def onMessage(self, msg, binary):
    data = json.loads(msg)
    model = self.factory.session.getModule(data['deviceId'])

    model.set('name', data['name'])
    model.set('sleep_interval_ms', data['sleep_interval_ms'])
    model.set('sit_interval_ms', data['sit_interval_ms'])

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

class PatientControlSocketFactory(WebSocketServerFactory):
  def __init__(self, url, session, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []
    self.session = session

    self.session.moduleIdList.on("change", self.sessionChange)
    self.session.bindAllModules("change:angle change:sleeping", self.updateData)
    self.session.bindAllModules("newTurn", self.updateTurn)

  def updateData(self, model, attr):
    message = {
      'type': 'update',
      'deviceId': model.get('deviceId'),
      'angle': model.get('angle'),
      'sleeping': model.get('sleeping')
    }
    self.broadcast(json.dumps(message))

  def updateTurn(self, model, turn):
    message = {
      'type': 'turn',
      'deviceId': model.get('deviceId'),
      'turn': turn
    }
    self.broadcast(json.dumps(message))

  def sessionChange(self, model, attr):
    self.broadcast(self.getState())

  def getState(self):
    state = json.dumps(self.session.moduleModels, default=lambda o: o.__dict__)
    stateDict = json.loads(state)
    stateDict['type'] = 'state'
    return json.dumps(stateDict)

  def register(self, client):
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, msg):
    for c in self.clients:
      c.sendMessage(msg)