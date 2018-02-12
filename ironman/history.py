from zope.interface import implements
from interfaces import IHistory

from constructs.ipbus import IPBusConstruct
import collections

class History(dict):
    implements(IHistory)

    def __init__(self, maxlen=100):
        self.maxlen = maxlen
        self.packets = collections.deque([None]*self.maxlen, maxlen=self.maxlen)

    def record(self, packet):
        # make sure packet doesn't exist first
        if packet in self.packets:
            raise ValueError("This packet has already been recorded in the history.")
        # Attempt to delete from history only if we are removing from queue
        if self.packets[0] is not None:
            del self[self.packets[0].request.header.id]
        # Add new packet to history
        self.packets.append(packet)
        self[packet.request.header.id] = (IPBusConstruct.build(packet.request).encode('hex'), IPBusConstruct.build(packet.response).encode('hex'))
        return packet
