from zope.interface import implements
from ironman.interfaces import IHardwareManager, IHardwareMap

class HardwareManager(object):
    implements(IHardwareManager)

    def check_data(self, address, data):
        pass

    def check_address(self, address):
        pass

    def find_address(self, address):
        pass

    def get_checksum(self, map_name):
        pass

    def add(self, hw_map):
        pass

class HardwareMap(object):
    implements(IHardwareMap)
