from zope.interface.verify import verifyClass, verifyObject
from ironman.packet import IPBusPacket
from ironman.interfaces import IIPBusPacket
from ironman.utilities import byteswap

IPBUS_VERSION = 2
BENDIAN_TESTPACKET = ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'
LENDIAN_TESTPACKET = '\xf0\x00\x00 \x0f\x01\x00 \x03\x00\x00\x00'

# fixtures for passing in the objects
import pytest

@pytest.mark.parametrize("data", [BENDIAN_TESTPACKET, LENDIAN_TESTPACKET])
def test_ipbus_packet_create(data):
    obj = IPBusPacket(data)
    assert obj is not None

def test_ipbus_packet_class_iface():
    # Assure the class implements the declared interface
    assert verifyClass(IIPBusPacket, IPBusPacket)

@pytest.mark.parametrize("data", [BENDIAN_TESTPACKET, LENDIAN_TESTPACKET])
def test_ipbus_packet_instance_iface(data):
    # Assure instances of the class provide the declared interface
    assert verifyObject(IIPBusPacket, IPBusPacket(data))

@pytest.mark.parametrize("data", [BENDIAN_TESTPACKET, LENDIAN_TESTPACKET])
def test_ipbus_packet_parse(data):
    # this should parse it all for us without erroring
    packet_normal = IPBusPacket(data)
    packet_swapped = IPBusPacket(byteswap(data))
    assert packet_normal.protocol_version == IPBUS_VERSION
    assert packet_normal.struct.header.reserved == 0x0
    assert packet_normal.packet_id == 0x0
    assert packet_normal.byteorder == 0xf
    assert packet_normal.packet_type == 'CONTROL'
    assert packet_normal.struct == packet_swapped.struct
