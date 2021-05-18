"""
    This file implements all of the various communications one might need to do.

    Jarvis provides a callback structure that looks up (in its registry) for an appropriate communication protocol.
"""

from zope.interface import implementer
from .interfaces import ICommunicationSlave, ICommunicationDriver, IHardwareNode
from .constructs.ipbus import IPBusWords


@implementer(ICommunicationSlave)
class Jarvis:
    """This is the general communication slave.

    Jarvis is what lets us pass around communications to various routes/protocols
    while keeping the details separated from us. Here's an example of how one might use it:

    >>> from ironman.communicator import Jarvis, SimpleIO
    >>> # create a Jarvis instance to manage what we want to register
    >>> j = Jarvis()
    >>> # tell Jarvis to register this class for the given route
    >>> @j.register('fpgaOne')
    ... class FileOne(SimpleIO):
    ...     __f__ = '/path/to/fileOne'
    ...
    >>> # tell Jarvis to register this class for the given route
    >>> @j.register('fpgaTwo')
    ... class FileTwo(SimpleIO):
    ...     __f__ = '/path/to/fileTwo'
    ...
    >>> # print the available registered classes
    >>> import pprint
    >>> pprint.pprint(j.registry)
    {'fpgaOne': <class 'ironman.communicator.FileOne'>,
     'fpgaTwo': <class 'ironman.communicator.FileTwo'>}

    Jarvis does the wrapping for :func:`Jarvis.register` so that a class defined at run-time is automatically inserted.

    """

    def __init__(self):
        self.registry = {}

    def set_hardware_manager(self, hwmanager):
        self.hwmanager = hwmanager

    def parse_address(self, address):
        return self.hwmanager.get_route(address)

    def __call__(self, packet):
        """
        Handle CONTROL packets
        """
        if packet.request.header.type_id == 'CONTROL':
            for transaction, response in zip(
                packet.request.transactions, packet.response.transactions
            ):
                response.data = self.__transaction__(transaction)
        return packet

    def __transaction__(self, transaction):
        protocol = self.registry.get(self.parse_address(transaction.address), None)
        if protocol is None:
            raise KeyError(transaction.address)
        protocol = protocol()
        if transaction.header.type_id == 'READ':
            return IPBusWords.parse(
                protocol.read(transaction.address, transaction.header.words)
            )
        elif transaction.header.type_id == 'WRITE':
            protocol.write(transaction.address, IPBusWords.build(transaction.data))
            return

    def register(self, route):
        if route is None:
            raise ValueError('Must specify a route')
        if route in self.registry:
            raise KeyError(
                "{:s} is an existing route to {:s}".format(
                    route, self.registry[route].__name__
                )
            )

        def register_wrapper(cls):
            """Duck-typing checks"""
            getattr(cls, 'read')
            getattr(cls, 'write')
            self.registry[route] = cls

        return register_wrapper

    def unregister(self, route):
        del self.registry[route]


@implementer(IHardwareNode)
class SimpleIO:
    __f__ = None

    def read(self, offset, size):
        with open(self.__f__, 'rb') as f:
            f.seek(offset)
            return f.read(4 * size)

    def write(self, offset, data):
        with open(self.__f__, 'r+b') as f:
            f.seek(offset)
            return f.write(data)


@implementer(ICommunicationDriver)
class ComplexIO:
    __f__ = {}

    def read(self, offset, size):
        with open(self.__f__.get(offset), 'rb') as f:
            return f.read(4 * size)

    def write(self, offset, data):
        with open(self.__f__.get(offset), 'r+b') as f:
            return f.write(data)
