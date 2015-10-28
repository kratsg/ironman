from twisted.internet.protocol import Factory, ServerFactory, Protocol, DatagramProtocol
from twisted.internet import reactor

class IPBusServerProtocol(DatagramProtocol, Protocol):
  def datagramReceived(self, datagram, address):
    print("Received udp")
    self.transport.write(datagram, address)

  def dataReceived(self, data):
    print("Received tcp")
    self.transport.write(data)

class IPBusServerFactory(ServerFactory):
  protocol = IPBusServerProtocol

class Packet(object):
  def __init__(self, data=None):
    self.packet_type = 1
    self.payload = ''
    self.structure = '!H6s'
    if data == None:
      return

    self.packet_type, self.payload = struct.unpack(self.structure, data)

  def pack(self):
    return struct.pack(self.structure, self.packet_type, self.payload)

  def __str__(self):
    return "Type: {0}\nPayload {1}\n\n".format(self.packet_type, self.payload)

def main():
  reactor.listenTCP(8000, IPBusServerFactory())
  reactor.listenUDP(8000, IPBusServerProtocol())

  reactor.run()

  reactor.stop()

if __name__ == '__main__':
  main()
