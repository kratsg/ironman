from zope.interface import implements
from ironman.interfaces import IHardwareManager, IHardwareMap, IHardwareNode
import xmltodict

class HardwareManager(dict):
    implements(IHardwareManager)

    def check_data(self, address, data):
        key, hw_map = self.find_address(address, data)
        return hw_map[address].isValueValid(data)

    def check_address(self, address):
        for key, hw_map in self.iteritems():
            if address in hw_map:
                return True
        return False

    def find_address(self, address):
        for key, hw_map in self.iteritems():
            if address in hw_map:
                return key, hw_map

    def get_checksum(self, map_name):
        pass

    def add(self, new_hw_map):
        """
            Add the HW map only if it doesn't exist for a given key, and no address collisions
        """
        if new_hw_map.key in self:
            raise KeyError("HW Map already exists: {0:s}".format(new_hw_map.key))
        for key, hw_map in self.iteritems():
            for new_address in new_hw_map.iterkeys():
                if new_address in hw_map:
                    raise ValueError("Address 0x{0:08x} ({0:d}) in {1:s} already exists in {2:s}".format(new_address, new_hw_map.key, key))
        # all ok, add it all
        self[new_hw_map.key] = new_hw_map

class HardwareMap(dict):
    implements(IHardwareMap)

    def __init__(self, xml, key):
        self.key = key
        self.parse(xml)

    def parse(self, xml):
        doc = xmltodict.parse(xml)
        # the doc is rather inflexible
        # top level is node
        for node in doc['node']['node']:
            # first check if the node has children, if it does, iterate over children
            nodeAddress = int(node['@address'], 16)
            if 'node' in node:
                children = node['node']
                # if there is only one node, it's not a list - fuck xml
                if not isinstance(children, list): children = [children]
                for child in children:
                    childAddress = int(child['@address'], 16)
                    absAddress = nodeAddress+childAddress
                    if absAddress in self: raise KeyError(child['@id'])
                    self[nodeAddress+childAddress] = HardwareNode(child)
            else:
                self[nodeAddress] = HardwareNode(node)

    def isOk(self):
        for k,v in self.iteritems():
            if not v.isOk(): return False
        return True

class HardwareNode(dict):
    implements(IHardwareNode)

    def __init__(self, node):
        #self['description'] = getattr(node, '@description', '')
        self['permissions'] = int(node.get('@permissions', 0))
        self['allowed'] = node.get('@allowed', [])
        self['disallowed'] = node.get('disallowed', ['-1'])

    @property
    def readable(self):
        return bool(self['permissions']&1)

    @property
    def writeable(self):
        return bool(self['permissions']&2)

    def isValueValid(self, val):
        return (self['allowed'] and val in self['allowed']) or \
               (self['disallowed'] and val not in self['disallowed'])

    @property
    def isOk(self):
        return (bool(self['allowed'])^bool(self['disallowed'])) and (self['permissions']&1)

    @property
    def permissions(self):
        return self['permissions']

    @property
    def allowed(self):
        return self['allowed']

    @property
    def disallowed(self):
        return self['disallowed']
