from zope.interface import implements
from ironman.interfaces import IHardwareManager, IHardwareMap, IHardwareNode
import xmltodict

class HardwareManager(dict):
    implements(IHardwareManager)
    raw_maps = {}

    def check_data(self, address, data):
        node = self.find_address(address)
        if node: return node.isValueValid(data)
        else: return False

    def check_address(self, address):
        node = self.find_address(address)
        if node: return True
        else: return False

    def find_address(self, address):
        return self.get(address, {})

    def get_checksum(self, map_name):
        pass

    def add(self, new_hw_map):
        """
            Add the HW map only if it doesn't exist for a given key, and no address collisions
        """
        new_route = new_hw_map.route
        if new_route in self.raw_maps:
            raise KeyError("HW Map already exists: {0:s}".format(new_hw_map.route))

        common_addresses = set(self).intersection(new_hw_map)
        if common_addresses:
            raise ValueError("An address in {0:s} already exists in the manager".format(new_route))
        # all ok, add it all
        self.raw_maps[new_route] = new_hw_map
        self.update(new_hw_map)

    def subtract(self, route):
        """
            Remove the route entirely.
        """
        for address in self.raw_maps.pop(route, {}).iterkeys():
            self.pop(address, None)

class HardwareMap(dict):
    implements(IHardwareMap)

    def __init__(self, xml, route):
        self.route = route
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

    def __init__(self, node, hw_map):
        #self['description'] = getattr(node, '@description', '')
        self['permissions'] = int(node.get('@permissions', 0))
        self['allowed'] = node.get('@allowed', [])
        self['disallowed'] = node.get('disallowed', ['-1'])
        self.hw_map = hw_map

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
