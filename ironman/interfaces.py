import zope.interface import Interface

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

class IIPbusPacket(Interface):
    """ IPBus Packet object
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
                0x0     Control packet
                0x1     Status packet
                0x2     Re-send request packet
                0x3-f   Reserved
        """

    def transaction_id():
        """ Transaction identification number
                Client/target can track each transaction for a given packet
        """

    def num_words():
        """ Number of 32-bit words within addressable memory space of the bus
            itself that are interacted with

            Defines read/write size of block reads/writes
        """

    def type_id():
        """
            Defines the type (read/write) of the IPBus transaction
        """

    def info_code():
        """
            Defines the direction and error state of the transaction
            request/response
                0x0     Request handled successfully by target
                0x1     Bad header
                0x2-3   Reserved
                0x4     Bus error on read
                0x5     Bus error on write
                0x6     Bus timeout on read
                0x7     Bus timeout on write
                0x8-e   Reserved
                0xf     Outbound request
        """

    def data():
        """ The data blob in the packet
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
