from zope.interface.verify import verifyClass, verifyObject
from ironman.server import IPBusServerProtocol
#from twisted.internet.interfaces import IProtocolFactory
#from twisted.pair.raw import IRawDatagramProtocol
from ironman.globals import TESTPACKETS, TESTRESPONSES
from twisted.internet.defer import Deferred

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

class TestIPBus:
    @pytest.fixture(autouse=True)
    def init_server(self):
        # an example response of how one might create the deferred
        def example_response(datagram):
            key = (key for key,value in TESTPACKETS.items() if value==datagram).next()
            return TESTRESPONSES[key]

        from twisted.test import proto_helpers
        self.echo_proto = IPBusServerProtocol(lambda: Deferred())
        #self.proto = IPBusServerProtocol(lambda: Deferred().addCallback(example_response))
        self.proto = IPBusServerProtocol(lambda: Deferred())
        self.tr = proto_helpers.FakeDatagramTransport()
        for pr in [self.echo_proto, self.proto]:
            pr.transport = self.tr
            pr.startProtocol()

    @pytest.mark.parametrize("inbound", [
        (TESTPACKETS['big-endian']),
        (TESTPACKETS['little-endian']),
    ])
    def test_echo(self, inbound):
        address, port = '127.0.0.1', 55555
        assert len(self.tr.written) == 0

        self.echo_proto.datagramReceived(inbound, (address, port))
        msg, addr = self.tr.written[0]
        assert msg == inbound
        assert addr[1] == port

    @pytest.mark.parametrize("inbound,expected", [
        (TESTPACKETS['big-endian'], TESTRESPONSES['big-endian']),
        (TESTPACKETS['little-endian'], TESTRESPONSES['little-endian']),
    ])
    def test_command(self, inbound, expected):
        address, port = '127.0.0.1', 55556
        assert len(self.tr.written) == 0

        self.proto.datagramReceived(inbound, (address, port))
        msg, addr = self.tr.written[0]
        assert msg == expected
        assert addr[1] == port
