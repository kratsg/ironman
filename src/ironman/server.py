# Server Class managing requests over udp
from twisted.internet.protocol import ServerFactory, Protocol, DatagramProtocol
import struct


class UDP(DatagramProtocol):
    def __init__(self, dgen):
        self.d = dgen

    def datagramReceived(self, datagram, address):
        """
        After receiving a datagram, generate the deferreds and add myself to it.
        """

        def write(result):
            print("Writing %r" % result)
            self.transport.write(result, address)

        d = self.d()
        # d.addCallbacks(write, log.err)
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
            print("Writing %r" % result)
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


class FauxCP(Protocol):
    def __init__(self, dgen):
        self.d = dgen

    def _stripPreIPBusHeader(self, data):
        return data[4:]

    def _addPreIPBusHeader(self, data):
        return struct.pack(">I", len(data)) + data

    def dataReceived(self, data):
        """
        After receiving the data, generate the deferreds and add myself to it.
        """

        def write(result):
            fauxResult = self._addPreIPBusHeader(result)
            print("Writing %r" % fauxResult)
            self.transport.write(fauxResult)

        d = self.d()
        d.addCallback(write)  # errors are silently ignored!
        d.callback(self._stripPreIPBusHeader(data))


class FauxFactory(ServerFactory):
    protocol = FauxCP

    def __init__(self, dgen):
        self.d = dgen

    def buildProtocol(self, addr):
        return self.protocol(self.d)


def ServerFactory(proto, dgen):
    if proto == 'udp':
        return UDP(dgen)
    elif proto == 'tcp':
        return TCPFactory(dgen)
    elif proto == 'fauxcp':
        return FauxFactory(dgen)
    else:
        return None
