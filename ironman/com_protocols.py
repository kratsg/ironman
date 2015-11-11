from zope.interface import implements
from ironman.interfaces import ICommunicationProtocol
from ironman.communicator import Jarvis

class SimpleIO(Jarvis):
    __route__ = 'file'
    __f__ = None
    implements(ICommunicationProtocol)

    def read(self, offset, size):
        with open(self.__f__, 'rb') as f:
            f.seek(offset)
            return f.read(size)

    def write(self, offset, data):
        with open(self.__f__, 'r+b') as f:
            f.seek(offset)
            return f.write(data)


