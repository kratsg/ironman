from zope.interface import Interface, Attribute


class IHistory(Interface):
    """Enhanced dictionary to store inbound and outbound packet pairs"""

    def record(packet):
        """record the packet"""


class IIPBusPacket(Interface):
    """IPBus Packet object"""

    request = Attribute("The parsed request packet")
    response = Attribute("The parsed response packet")
    _raw = Attribute("The raw request packet")
    raw = Attribute("The raw datagram blob.")
    protocol_version = Attribute(
        "The packet header protocol version. This does not check that the encapsulated transactions also match."
    )
    reserved = Attribute("Reserved. Should be 0x0.")
    packet_id = Attribute("The id of the ipbus packet.")
    byteorder = Attribute("The byte-order in the header. Should assert == 0xf.")
    packet_type = Attribute(
        """The type of packet.

            ======= ===============
            Value   Type
            ======= ===============
            0x0     Control
            0x1     Status
            0x2     Re-send request
            0x3-f   Reserved
            ======= ==============="""
    )
    response = Attribute(
        "The data response to be passed along to another function that builds the response packet. This should be a list [] to append responses to."
    )

    def __init__(blob):
        """Packet is initialized with a data blob
        to decode. Determine if it is big or little endian.
        """

    def __eq__(other):
        """Define a way to identify two packets as being equivalent. Best way is to compare the underlying structs"""

    def __ne__(other):
        """This should just be :code:`return not self.__eq__(other)`."""


class IHardwareManager(Interface):
    """Our Hardware Maps manager"""

    raw_maps = Attribute(
        "A dictionary of the maps added so we can keep track which makes it easier to add and remove."
    )

    def get_node(address):
        """Given an address, return the node associated with it"""

    def get_route(address):
        """Given an address, return the route for it"""

    def get_checksum(route):
        """Look up the checksum for a given map name (route)"""

    def check_address(address):
        """Given an address, checks if it is valid"""

    def check_data(address, data):
        """Given an address, checks if the data is
        a valid value to write
        """

    def add(hw_map):
        """Add the Map object to the Hardware"""

    def subtract(route):
        """Remove the route from the hardware manager"""


class IHardwareMap(Interface):
    """Manages information about a single map, should be an overloaded dictionary"""

    route = Attribute("The route associated for this hardware map.")

    def __init__(xml, route):
        """Initialize a hardware map object by giving it the data to parse and associate it with a route"""

    def parse(xml):
        """Parse the xml hardware map data to set things up"""

    def isOk():
        """Whether or not the given hardware map is ok. Should just be a loop over :func:`IHardwareNode.isOk`."""


class IHardwareNode(Interface):
    """Manages information about a single address. Simply a well-defined dictionary."""

    # description = Attribute("A description of the node.")
    permissions = Attribute("Mark the node's read/write capabilities.")
    allowed = Attribute("A list of allowed values for the node.")
    disallowed = Attribute("A list of disallowed values for the node.")
    readable = Attribute("Is the given node readable?")
    writeable = Attribute("Is the given node writeable?")
    isOk = Attribute(
        "Is the given node ok? EG: can't set allowed and disallowed objects at the same time and cannot block a node from being readable."
    )
    hw_map = Attribute("The hardware map this is associated with.")

    def __init__(node, hw_map):
        """Initialize the node by giving it the parsed xml data as well as the hw_map"""

    def isValueValid(val):
        """Whether the given value is a valid value for the node"""


class ICommunicationSlave(Interface):
    """Manages the communication with the programmable logic for us"""

    def set_hardware_manager(hwmanager):
        """Set the hardware manager that the slave communications with"""

    def parse_address(address):
        """Parses address and returns what function to call"""

    def __call__(packet):
        """A non-blocking I/O call passing along the packet

        Returns the responses
        """

    def __transaction__(transaction):
        """Handle a single transaction and return the response"""


class ICommunicationDriver(Interface):
    """The standard driver that is expected for all methods of communication on the board"""

    def read(offset, size):
        """Read from the given address (offset) for N bytes (size)"""

    def write(offset, value):
        """Write to the given address (offset) for N bytes (len(value))"""
