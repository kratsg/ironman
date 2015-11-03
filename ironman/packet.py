# Packet object that manages the formats of our packets
# http://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined

from zope.interface import implements
from interfaces import IIPBusPacket
from utilities import byteswap

from constructs.ipbus import IPBusConstruct

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
        if self.littleendian:
            return byteswap(self.raw)
        return self.raw

    @property
    def raw(self):
        return self._blob

    @property
    def protocol_version(self):
        return self.struct.header.protocol_version

    @property
    def packet_id(self):
        return self.struct.header.id

    @property
    def byteorder(self):
        return self.struct.header.byteorder

    @property
    def packet_type(self):
        return self.struct.header.type_id
