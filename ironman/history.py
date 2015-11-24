from zope.interface import implements
from interfaces import IHistory

from constructs.ipbus import IPBusConstruct

class History(dict):
    implements(IHistory)

    def record(self, packet):
        self[packet.request.header.id] = (IPBusConstruct.build(packet.request), IPBusConstruct.build(packet.response))
