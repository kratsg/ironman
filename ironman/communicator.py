"""
    This file implements all of the various communications one might need to do.

    Jarvis provides a callback structure that looks up (in its registry) for an appropriate communication protocol.
"""

from zope.interface import implements
from ironman.interfaces import ICommunicationSlave

class CommunicationSlaveManager(type):
    # we use __init__ rather than __new__ here because we want
    # to modify attributes of the class *after* they have been
    # created
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            # this is the base class.  Create an empty registry
            cls.registry = {}
        else:
            # this is a derived class.  Add cls to the registry
            cls.register()

        super(CommunicationSlaveManager, cls).__init__(name, bases, dct)

    def register(cls):
        """ Register the given class in the slave as a route.
            The route it matches should be given by __route__ in the class declaration.
        """
        cls.registry[cls.__route__] = cls

class Jarvis(object):
    __metaclass__ = CommunicationSlaveManager
    implements(ICommunicationSlave)

    def __init__(self, hwmanager):
        self.hwmanager = hwmanager

    def parse_address(self, address):
        return hwmanager.parse_address(address)

    def __call__(self, packet):
        return self.registry[self.parse_address(packet.transaction.address)]
