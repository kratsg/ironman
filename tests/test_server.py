from zope.interface.verify import verifyClass, verifyObject
from ironman.server import IPBusServerProtocol, IPBusServerFactory
from twisted.internet.interfaces import IProtocol, IProtocolFactory

# fixtures for passing in the objects
import pytest

class TestServerProtocol:
    def test_server_protocol_create(self):
        obj = IPBusServerProtocol()
        assert obj is not None

    def test_server_protocol_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(IProtocol, IPBusServerProtocol)

    def test_server_protocol_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(IProtocol, IPBusServerProtocol())

class TestServerFactory:
    def test_server_factory_create(self):
        obj = IPBusServerFactory()
        assert obj is not None

    def test_server_factory_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(IProtocolFactory, IPBusServerFactory)

    def test_server_factory_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(IProtocolFactory, IPBusServerFactory())

@pytest.fixture
def ipbus_server():
    from twisted.test import proto_helpers
    factory = IPBusServerFactory()
    protocol = factory.buildProtocol(('127.0.0.1', 0))
    transport = proto_helpers.StringTransport()
    protocol.makeConnection(transport)

class TestIPBus:
    @pytest.fixture(autouse=True)
    def init_server(self):
        from twisted.test import proto_helpers
        factory = IPBusServerFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(tr)

    @pytest.mark.parametrize("inbound,expected", [
        ("write", "written"),
        ("read", "value"),
    ])
    def test_command(self, inbound, expected):
        self.proto.dataReceived(inbound)
        assert self.tr.value == expected
