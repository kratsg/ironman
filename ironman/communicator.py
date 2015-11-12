"""
    This file implements all of the various communications one might need to do.

    Jarvis provides a callback structure that looks up (in its registry) for an appropriate communication protocol.
"""

from zope.interface import implements
from ironman.interfaces import ICommunicationSlave, ICommunicationProtocol

class Jarvis(object):
    """ This is the general communication slave.

        Jarvis is what lets us pass around communications to various routes/protocols
        while keeping the details separated from us. Here's an example of how one might use it::

            from ironman.communicator import Jarvis, SimpleIO
            # create a Jarvis instance to manage what we want to register
            j = Jarvis()

            # tell Jarvis to register this class' instance when we give it a route
            @j.register
            class FileOne(SimpleIO):
                __f__ = '/path/to/fileOne'

            # tell Jarvis to register this class' instance when we give it a route
            @j.register
            class FileTwo(SimpleIO):
                __f__ = '/path/to/fileTwo'

            # simultaneously provide a route (`fpgaOne`, `fpgaTwo`) while instantiating the class
            FileOne('fpgaOne')
            FileTwo('fpgaTwo')

            # print the available registered classes
            print j.registry

        Jarvis does the wrapping for :func:`Jarvis.register` by writing a :class:`JarvisWrapper` class that wraps around the original class you define.
    """
    implements(ICommunicationSlave)

    def __init__(self):
        self.registry = {}

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

    def register(self, cls):
        def register_wrapper(route=None):
            if route is None:
                ValueError('Must specify a route')
            if route in self.registry:
                KeyError(route)
            class JarvisWrapper(cls):
                def __init__(inner_self, *cls_args, **cls_kwargs):
                    self.registry[route] = inner_self
                    super(JarvisWrapper, inner_self).__init__(*cls_args, **cls_kwargs)

                def __repr__(inner_self):
                    currRepr = super(JarvisWrapper, inner_self).__repr__()
                    return currRepr.replace('ironman.communicator.JarvisWrapper', cls.__name__)
            return JarvisWrapper()
        return register_wrapper

class SimpleIO(object):
    implements(ICommunicationProtocol)
    __f__ = None

    def read(self, offset, size):
        with open(self.__f__, 'rb') as f:
            f.seek(offset)
            return f.read(size)

    def write(self, offset, data):
        with open(self.__f__, 'r+b') as f:
            f.seek(offset)
            return f.write(data)
