import zope.interface import Interface

class IPacket(Interface):
    """ Packet object
    """

class IHardware(Interface):
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
