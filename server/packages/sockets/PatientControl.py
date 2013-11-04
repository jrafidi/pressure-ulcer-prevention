from autobahn.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

class PatientControlProtocol(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)
    # TODO: send initial state message to web UI
    pass

  def onMessage(self, msg, binary):
    # TODO: handle patient setting from web UI
    pass

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

class PatientControlSocketFactory(WebSocketServerFactory):
  def __init__(self, url, session, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []
    self.session = session

    # TODO: listen to session changes

  def sessionChange(self, model, attr):
    # TODO: broadcast changes to the session
    pass

  def dataUpdate(self, model, attr):
    # TODO: send up real-time data for the connected modules
    pass

  def register(self, client):
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, msg):
    for c in self.clients:
      c.sendMessage(msg)