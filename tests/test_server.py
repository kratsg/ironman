from zope.interface.verify import verifyClass, verifyObject
from ironman.server import IPBusServerProtocol, IPBusServerFactory
from twisted.internet.interfaces import IProtocol, IProtocolFactory

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
