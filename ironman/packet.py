# Packet object that manages the formats of our packets
# http://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined

from zope.interface import implements
from ironman.interfaces import IIPBusPacket

class IPBusPacket(object):
    implements(IIPBusPacket)

    def __init__(blob):
        self.blob = blob
        self.data = []
        self.endianness = ">" # assume big-endian
        if not (self.__parse(self.blob[:4])>>4)&0xf == 0xf:
            self.endianness = "<"
        for i in range(0, len(blob), 4):
            self.data.append(self.__unpack(i))

    def __unpack(start=0):
        return struct.unpack("{0:s}I".format(self.endianness), blob[start:start+4])[0]

    def __pack():
        return struct.pack("{0:s}I".format(self.endianness), self.data)

# an alternate way that is easier to manage!
from construct import Struct, BitStruct, BitField

data = '\xf0\x00\x00 \x0f\x01\x00 \x03\x00\x00\x00'
#data = ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'

# byte-swapping needed
if (ord(data[0])&0xf0)>>4 == 0xf:
    temp_data = []
    for i in range(0, len(data), 4):
        temp_data.append(''.join(reversed(data[i:i+4])))
    data = ''.join(temp_data)

ipbus_packet = Struct("IPBusPacket",
                BitStruct("packet_header",
                    BitField("protocol_version", 4),
                    BitField("reserved", 4),
                    BitField("packet_id", 16),
                    BitField("byteorder", 4),
                    BitField("packet_type", 4)
                    )
                )

print ipbus_packet.parse(data)
