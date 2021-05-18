# Packet object that manages the formats of our packets
# http://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined

from zope.interface import implementer
from .interfaces import IIPBusPacket

from .constructs.ipbus import IPBusConstruct


@implementer(IIPBusPacket)
class IPBusPacket:
    def __init__(self, blob):
        self.request = None
        self.response = None
        self._raw = blob
        raw = self.raw
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
        return isinstance(other, self.__class__) and self.request == other.request

    def __ne__(self, other):
        return not self.__eq__(other)
