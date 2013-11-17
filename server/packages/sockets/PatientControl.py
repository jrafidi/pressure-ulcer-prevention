from autobahn.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

import json

class PatientControlProtocol(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)
    self.sendMessage(self.factory.getState())

  def onMessage(self, msg, binary):
    # TODO: handle patient setting from web UI
    print msg

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

class PatientControlSocketFactory(WebSocketServerFactory):
  def __init__(self, url, session, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []
    self.session = session

    self.session.moduleIdList.on("change", self.sessionChange)
    self.session.bindAllModules("change:angle", self.updateData)

  def updateData(self, model, attr):
    message = "{\"" + model.get("deviceId") + "\":" + str(model.get(attr)) + "}"
    self.broadcast(message)

  def sessionChange(self, model, attr):
    self.broadcast(self.getState())

  def getState(self):
    state = json.dumps(self.session.moduleModels, default=lambda o: o.__dict__)
    return state

  def register(self, client):
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, msg):
    for c in self.clients:
      c.sendMessage(msg)