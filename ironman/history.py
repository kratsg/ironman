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
        # Attempt to delete from history only if we are removing from queue
        if len(self.packets) >= self.maxlen:
            del self[self.packets[0].request.header.id]
        # Add new packet to history
        self.packets.append(packet)
        self[packet.request.header.id] = (IPBusConstruct.build(packet.request), IPBusConstruct.build(packet.response))
