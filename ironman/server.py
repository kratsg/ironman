# Server Class managing requests over udp
from twisted.internet.protocol import DatagramProtocol
from twisted.internet.protocol import ServerFactory, Protocol, DatagramProtocol

class UDP(DatagramProtocol):
    def __init__(self, dgen):
        self.d = dgen

    def datagramReceived(self, datagram, address):
        """
        After receiving a datagram, generate the deferreds and add myself to it.
        """
        def write(result):
            print "Writing %r" % result
            self.transport.write(result, address)

        d = self.d()
        #d.addCallbacks(write, log.err)
        d.addCallback(write)  # errors are silently ignored!
        d.callback(datagram)

class TCP(Protocol):
    def __init__(self, dgen):
        self.d = dgen

    def dataReceived(self, data):
        """
        After receiving the data, generate the deferreds and add myself to it.
        """
        def write(result):
            print "Writing %r" % result
            self.transport.write(result)
        d = self.d()
        d.addCallback(write)  # errors are silently ignored!
        d.callback(data)

class TCPFactory(ServerFactory):
    protocol = TCP
    def __init__(self, dgen):
        self.d = dgen

    def buildProtocol(self, addr):
        return self.protocol(self.d)


def ServerFactory(proto, dgen):
    if proto == 'udp':
        return UDP(dgen)
    elif proto == 'tcp':
        return TCPFactory(dgen)
    else:
        return None
