# Packet object that manages the formats of our packets
# http://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined

from zope.interface import implements
from interfaces import IIPBusPacket
from utilities import byteswap

from constructs.ipbus import IPBusConstruct

class IPBusPacket(object):
    implements(IIPBusPacket)

    def __init__(self, blob):
        self.request = None
        self.response = None
        self._raw = blob
        # if little-endian, we need to swap when reading and writing
        self.littleendian = bool((ord(self._raw[0])&0xf0)>>4 == 0xf)
        # do some flipping
        raw = self.raw
        if self.littleendian: raw = byteswap(raw)
        self.request = IPBusConstruct.parse(raw)
        self.response = IPBusConstruct.parse(raw)

    @property
    def raw(self):
        return self._raw

    @property
    def protocol_version(self):
        return self.request.header.protocol_version

    @property
    def reserved(self):
        return self.request.header.reserved

    @property
    def packet_id(self):
        return self.request.header.id

    @property
    def byteorder(self):
        return self.request.header.byteorder

    @property
    def packet_type(self):
        return self.request.header.type_id

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.request == other.request)

    def __ne__(self, other):
        return not self.__eq__(other)
