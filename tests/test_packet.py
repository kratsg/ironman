from zope.interface.verify import verifyClass, verifyObject
from ironman.packet import IPBusPacket
from ironman.interfaces import IIPbusPacket

def test_ipbus_packet_create():
    obj = IPBusPacket()
    assert obj is not None

def test_ipbus_packet_class_iface():
    # Assure the class implements the declared interface
    assert verifyClass(IIPBusPacket, IPBusPacket)

def test_ipbus_packet_instance_iface():
    # Assure instances of the class provide the declared interface
    assert verifyObject(IIPBusPacket, IPBusPacket())
