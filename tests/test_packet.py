from zope.interface.verify import verifyClass, verifyObject
from ironman.packet import IPBusPacket
from ironman.interfaces import IIPBusPacket

def test_ipbus_packet_create():
    obj = IPBusPacket()
    assert obj is not None

def test_ipbus_packet_class_iface():
    # Assure the class implements the declared interface
    assert verifyClass(IIPBusPacket, IPBusPacket)

def test_ipbus_packet_instance_iface():
    # Assure instances of the class provide the declared interface
    assert verifyObject(IIPBusPacket, IPBusPacket())

# test packets using the following:
# little endian packet
#data = '\xf0\x00\x00 \x0f\x01\x00 \x03\x00\x00\x00'
# big endian packet
#data = ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'

