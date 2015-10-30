# Packet object that manages the formats of our packets
# http://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined

from zope.interface import implements
from ironman.interfaces import IIPBusPacket

class IPBusPacket(object):
    implements(IIPBusPacket)
    pass
