from zope.interface.verify import verifyClass, verifyObject
from ironman.server import IPBusServerProtocol, IPBusServerFactory
#from twisted.internet.interfaces import IProtocolFactory
#from twisted.pair.raw import IRawDatagramProtocol

# fixtures for passing in the objects
import pytest

#class TestServerProtocol:
#    def test_server_protocol_create(self):
#        obj = IPBusServerProtocol()
#        assert obj is not None
#
#    def test_server_protocol_class_iface(self):
#        # Assure the class implements the declared interface
#        assert verifyClass(IRawDatagramProtocol, IPBusServerProtocol)
#
#    def test_server_protocol_instance_iface(self):
#        # Assure instances of the class provide the declared interface
#        assert verifyObject(IRawDatagramProtocol, IPBusServerProtocol())
#
#class TestServerFactory:
#    def test_server_factory_create(self):
#        obj = IPBusServerFactory()
#        assert obj is not None
#
#    def test_server_factory_class_iface(self):
#        # Assure the class implements the declared interface
#        assert verifyClass(IProtocolFactory, IPBusServerFactory)
#
#    def test_server_factory_instance_iface(self):
#        # Assure instances of the class provide the declared interface
#        assert verifyObject(IProtocolFactory, IPBusServerFactory())

class TestIPBus:
    @pytest.fixture(autouse=True)
    def init_server(self):
        from twisted.test import proto_helpers
        factory = IPBusServerFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.FakeDatagramTransport()
        self.proto.transport = self.tr
        self.proto.startProtocol()

    @pytest.mark.parametrize("inbound,expected,shouldPass", [
        ("write", "written", True),
        ("read", "value", True),
        ("read", "fake", False),
    ])
    def test_command(self, inbound, expected, shouldPass):
        address, port = '127.0.0.1', 55555
        assert len(self.tr.written) == 0

        self.proto.datagramReceived(inbound, (address, port))
        msg, addr = self.tr.written[0]
        assert (msg == expected) == shouldPass
        assert addr[1] == port
