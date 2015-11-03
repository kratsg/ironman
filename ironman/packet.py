# Packet object that manages the formats of our packets
# http://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined

from zope.interface import implements
from interfaces import IIPBusPacket
from utilities import byteswap

from constructs import IPBusConstruct

class IPBusPacket(object):
    implements(IIPBusPacket)

    def __init__(self, blob):
        self._blob = blob
        # if little-endian, we need to swap when reading and writing
        self.littleendian = bool((ord(self._blob[0])&0xf0)>>4 == 0xf)

    @property
    def struct(self):
        return IPBusConstruct.parse(self.blob)

    @property
    def blob(self):
        """ Return the big-endian datagram blob.
        """
        if self.littleendian:
            return byteswap(self.raw)
        return self.raw

    @property
    def raw(self):
        """ Return the raw datagram blob.
        """
        return self._blob

    @property
    def protocol_version():
        return self.struct.header.protocol_version

    def packet_id():
        return self.struct.header.id

    def byteorder():
        return self.struct.header.byteorder

    def packet_type():
        return self.struct.header.type_id
