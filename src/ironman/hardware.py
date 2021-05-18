from zope.interface import implementer
from .interfaces import IHardwareManager, IHardwareMap, IHardwareNode
import yaml


@implementer(IHardwareManager)
class HardwareManager(dict):
    raw_maps = {}

    def check_data(self, address, data):
        node = self.get_node(address)
        return node.isValueValid(data)

    def check_address(self, address):
        return not isinstance(self.get_node(address), NullHardwareNode)

    def find_address(self, address):
        return self.get(address, NullHardwareNode())

    def get_route(self, address):
        return self.get_node(address).hw_map.route

    def get_node(self, address):
        return self.get(address, NullHardwareNode())

    def get_checksum(self, map_name):
        pass

    def add(self, new_hw_map):
        """
        Add the HW map only if it doesn't exist for a given key, and no address collisions
        """
        new_route = new_hw_map.route
        if new_route in self.raw_maps:
            raise KeyError("HW Map already exists: {:s}".format(new_hw_map.route))

        common_addresses = set(self).intersection(new_hw_map)
        if common_addresses:
            raise ValueError(
                "An address in {:s} already exists in the manager".format(new_route)
            )
        # all ok, add it all
        self.raw_maps[new_route] = new_hw_map
        self.update(new_hw_map)

    def subtract(self, route):
        """
        Remove the route entirely.
        """
        for address in self.raw_maps.pop(route, NullHardwareMap()).iterkeys():
            self.pop(address, NullHardwareNode())


class BlockMemHardwareManager(HardwareManager):
    def get_node(self, address):
        blk = (
            self.get(address)
            if address in self
            else self.get(min(self.keys(), key=lambda k: abs(k - address)))
        )
        if blk is not None and address <= blk.node.get('address') + blk.node.get(
            'size', 0
        ):
            return blk
        else:
            return NullHardwareNode()


@implementer(IHardwareMap)
class NullHardwareMap(dict):
    route = None

    def parse(self, yml):
        pass

    def isOk(self):
        return False


@implementer(IHardwareMap)
class HardwareMap(dict):
    def __init__(self, yml, route):
        self.route = route
        self.parse(yml)

    def parse(self, yml):
        doc = yaml.load(yml)
        for node in doc.get('nodes', []):
            baseAddress = node.get('address')
            # this will check if there are any children later
            child = None
            for child in node.get('nodes', []):
                childAddress = child.get('address')
                absAddress = baseAddress + childAddress
                if absAddress in self:
                    raise KeyError('{:s}/{:s}'.format(node['id'], child['id']))
                self[absAddress] = HardwareNode(child, self)
            # no children
            if child is None:
                self[baseAddress] = HardwareNode(node, self)

    def isOk(self):
        for k, v in self.iteritems():
            if not v.isOk():
                return False
        return True


@implementer(IHardwareMap)
class NullHardwareNode(dict):

    hw_map = NullHardwareMap()
    readable = False
    writeable = False
    isValueValid = False
    isOk = False
    permissions = set()
    allowed = set()
    disallowed = set()


@implementer(IHardwareNode)
class HardwareNode(dict):
    def __init__(self, node, hw_map):
        # self['description'] = getattr(node, 'description', '')
        self['permissions'] = int(node.get('permissions', 0))
        self['allowed'] = node.get('allowed', [])
        self['disallowed'] = node.get('disallowed', ['-1'])
        self.hw_map = hw_map
        self.node = node

    @property
    def readable(self):
        return bool(self['permissions'] & 1)

    @property
    def writeable(self):
        return bool(self['permissions'] & 2)

    def isValueValid(self, val):
        return (self['allowed'] and val in self['allowed']) or (
            self['disallowed'] and val not in self['disallowed']
        )

    @property
    def isOk(self):
        return (bool(self['allowed']) ^ bool(self['disallowed'])) and (
            self['permissions'] & 1
        )

    @property
    def permissions(self):
        return self['permissions']

    @property
    def allowed(self):
        return self['allowed']

    @property
    def disallowed(self):
        return self['disallowed']
