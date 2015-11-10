"""
    This file implements all of the various communications one might need to do.

    Jarvis provides a callback structure that looks up (in its registry) for an appropriate communication protocol.
"""

from zope.interface import implements
from ironman.interfaces import ICommunicationSlave, ICommunicationProtocol

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

    def set_hardware_manager(self, hwmanager):
        self.hwmanager = hwmanager

    def parse_address(self, address):
        return self.hwmanager.parse_address(address)

    def __call__(self, packet):
        for transaction in packet.struct.data:
            packet.response.append(self.__transaction__(transaction))
        return packet

    def __transaction__(self, transaction):
        protocol = self.registry.get(self.parse_address(transaction.address), None)
        if protocol is None:
            KeyError(transaction.address)
        protocol = protocol()
        if transaction.type_id == 'READ':
            return protocol.read(transaction.address, transaction.words)
        elif transaction.type_id == 'WRITE':
            return protocol.write(transaction.address, transaction.data)

class SimpleIO(Jarvis):
    __route__ = 'file'
    __f__ = '/Users/kratsg/Desktop/SimpleIO'
    implements(ICommunicationProtocol)

    def read(self, offset, size):
        with open(self.__f__, 'rb') as f:
            f.seek(offset)
            return f.read(size)

    def write(self, offset, data):
        with open(self.__f__, 'r+b') as f:
            f.seek(offset)
            return f.write(data)


