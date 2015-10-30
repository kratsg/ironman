# Server Class managing requests over udp
from twisted.internet.protocol import ServerFactory, DatagramProtocol

class IPBusServerProtocol(DatagramProtocol):
    pass

class IPBusServerFactory(ServerFactory):
    pass
