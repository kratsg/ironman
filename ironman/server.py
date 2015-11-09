# Server Class managing requests over udp
from twisted.internet.protocol import DatagramProtocol

class IPBusServerProtocol(DatagramProtocol):
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
