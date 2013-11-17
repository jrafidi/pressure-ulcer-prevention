from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import listenWS

from packages.sockets.PatientControl import *
from packages.sockets.PatientModule import *

from packages.model.Session import *

WEBSOCKET_PORT = 8000
SOCKET_PORT = 7123
WEB_PORT = 81

if __name__ == '__main__':
  # Create the session
  session = Session()

  # Setup websocket protocol for patient control
  factory = PatientControlSocketFactory("ws://localhost:" + str(WEBSOCKET_PORT), session, debug = False)
  factory.protocol = PatientControlProtocol
  listenWS(factory)

  # Setup socket registration for patient modules
  reactor.listenTCP(SOCKET_PORT, PatientModuleSocketFactory(session))

  # Setup static html serving
  resource = File('../interface')
  staticServerFactory = Site(resource)
  reactor.listenTCP(WEB_PORT, staticServerFactory)
  reactor.run()