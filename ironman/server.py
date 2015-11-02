# Server Class managing requests over udp
from twisted.internet.protocol import ServerFactory, DatagramProtocol

class IPBusServerProtocol(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        print("Received udp from {1:s}\n\t{0:s}".format(datagram, address))
        if datagram == "write":
            self.transport.write("written", address)
        elif datagram == "read":
            self.transport.write("value", address)
        else:
            self.transport.write(datagram, address)

class IPBusServerFactory(ServerFactory):
    protocol = IPBusServerProtocol
