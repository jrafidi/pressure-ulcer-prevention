from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import listenWS

from packages.sockets.PatientControl import *
from packages.sockets.PatientModule import *

from packages.model.Session import *

if __name__ == '__main__':
  # Create the session
  session = Session()

  # Setup websocket protocol for patient control
  factory = PatientControlSocketFactory("ws://localhost:9000", session, debug = False)
  factory.protocol = PatientControlProtocol
  listenWS(factory)

  # Setup socket registration for patient modules
  reactor.listenTCP(8123, PatientModuleSocketFactory(session))

  # Setup static html serving
  resource = File('../interface')
  staticServerFactory = Site(resource)
  reactor.listenTCP(80, staticServerFactory)
  reactor.run()