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

