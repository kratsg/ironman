from zope.interface import Interface, Attribute

class IPacketStorage(Interface):
    """ Basic enhanced dictionary to centrally manage all packet data
    """

    def record(packet):
        """ record the packet
        """

class IHistory(Interface):
    """ Enhanced dictionary to store inbound and outbound packet pairs
    """

    def record(inbound_packet, outbound_packet):
        """ record both packets
        """

class IIPBusPacket(Interface):
    """ IPBus Packet object
    """
    _blob = Attribute("The data blob that this packet corresponds to")
    littleendian = Attribute("A flag dictating whether the datagram is received/sent in little-endian.")

    def __init__(blob):
        """ Packet is initialized with a data blob
            to decode. Determine if it is big or little endian.
        """

    def struct():
        """ The C-type struct representation of the packet.
        """

    def blob():
        """ Return the big-endian datagram blob.
        """

    def raw():
        """ Return the raw datagram blob.
        """

    def protocol_version():
        """ Protocol version
        """

    def packet_id():
        """ Packet ID
        """

    def byteorder():
        """ Endian-ness
        """

    def packet_type():
        """ Type of packet

            ======= ===============
            Value   Type
            ======= ===============
            0x0     Control
            0x1     Status
            0x2     Re-send request
            0x3-f   Reserved
            ======= ===============
        """

class IHardwareManager(Interface):
    """ Our Hardware Maps manager
    """
    def check_data(address, data):
        """ Given an address, checks if the data is
            a valid value to write
        """

    def check_address(address):
        """ Given an address, checks if it is valid
        """

    def find_address(address):
        """ Look up an address, return Error if cannot find
        """

    def get_checksum(map_name):
        """ Look up the checksum for a given map name
        """

    def add(map):
        """ Add the Map object to the Hardware
        """

class IHardwareMap(Interface):
    """ Manages information about a single map, should be an overloaded dictionary
    """

class ICommunicationSlave(Interface):
    """ Manages the communication with the programmable logic for us
    """
    def parse_address(address):
        """ Parses address and returns what function to call
        """

    def do_sdio():
        """ Communicate over SDIO
        """

    def do_gpio():
        """ Communicate over GPIO
        """

    def do_i2c():
        """ Communicate over I2C
        """

    def do_spi():
        """ Communicate over SPI
        """
