from zope.interface.verify import verifyClass, verifyObject
from ironman.packet import IPBusPacket
from ironman.interfaces import IIPBusPacket
from ironman.utilities import byteswap

IPBUS_VERSION = 2
BENDIAN_TESTPACKET = ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'
LENDIAN_TESTPACKET = '\xf0\x00\x00 \x0f\x01\x00 \x03\x00\x00\x00'
COMPLEXCONTROL_TESTPACKET = '\xf0\x00\x00 \x1f\x01\x00 \x06\x00\x00\x00\x00\x00\x00\x00\x1f\x01\x01 \x06\x00\x00\x00\x01\x00\x00\x00\x0f\x01\x02 \x03\x00\x00\x00'

# fixtures for passing in the objects
import pytest

@pytest.mark.parametrize("data", [BENDIAN_TESTPACKET, LENDIAN_TESTPACKET], ids=["big-endian packet", "little-endian packet"])
def test_ipbus_packet_create(data):
    obj = IPBusPacket(data)
    assert obj is not None

def test_ipbus_packet_class_iface():
    # Assure the class implements the declared interface
    assert verifyClass(IIPBusPacket, IPBusPacket)

@pytest.mark.parametrize("data", [BENDIAN_TESTPACKET, LENDIAN_TESTPACKET], ids=["big-endian packet", "little-endian packet"])
def test_ipbus_packet_instance_iface(data):
    # Assure instances of the class provide the declared interface
    assert verifyObject(IIPBusPacket, IPBusPacket(data))

class TestIPBusControlPacketParse:
    @pytest.fixture(autouse=True,
                    params=[BENDIAN_TESTPACKET, LENDIAN_TESTPACKET, COMPLEXCONTROL_TESTPACKET],
                    ids=["big-endian packet", "little-endian packet", "complex control packet"])
    def init_packet(self, request):
        self.packet = IPBusPacket(request.param)

    def test_protocol_version(self):
        assert self.packet.protocol_version == IPBUS_VERSION

    def test_header_reserved(self):
        assert self.packet.reserved == 0x0

    def test_packet_id(self):
        assert self.packet.packet_id == 0x0

    def test_byteorder(self):
        assert self.packet.byteorder == 0xf

    def test_control_type(self):
        assert self.packet.packet_type == 'CONTROL'

    def test_packet_swap(self):
        swapped_packet = IPBusPacket(byteswap(self.packet.raw))
        assert self.packet == swapped_packet

class TestIPBusControlPacketSimpleParse:
    @pytest.fixture(autouse=True)
    def init_packet(self):
        self.packet = IPBusPacket(BENDIAN_TESTPACKET)

    def test_length(self):
        assert len(self.packet.struct.data) == 1

    # specify details about inside packets
    @pytest.fixture(params=[(0, 'READ', )], ids=["first"])
    def packet_details(self, request):
        return request.param

    def test_transaction_type_id(self, packet_details):
        i, type_id = packet_details
        assert self.packet.struct.data[i].transaction.type_id == type_id

    def test_transaction_id(self, packet_details):
        i, _ = packet_details
        assert self.packet.struct.data[i].transaction.id == i

    def test_transaction_num_words(self, packet_details):
        i, _ = packet_details
        assert self.packet.struct.data[i].transaction.words == 0x1

    def test_transaction_info_code(self, packet_details):
        i, _ = packet_details
        assert self.packet.struct.data[i].transaction.info_code == 'REQUEST'

class TestIPBusControlPacketComplexParse:
    @pytest.fixture(autouse=True)
    def init_packet(self):
        self.packet = IPBusPacket(COMPLEXCONTROL_TESTPACKET)

    def test_length(self):
        assert len(self.packet.struct.data) == 3

    @pytest.fixture(params=[(0, 'WRITE', 0x6, [0x0]), (1, 'WRITE', 0x6, [0x1]), (2, 'READ', 0x3, None)], ids=["first", "second", "third"])
    def packet_details(self, request):
        return request.param

    def test_transaction_type_id(self, packet_details):
        i, type_id, _, _ = packet_details
        assert self.packet.struct.data[i].transaction.type_id == type_id

    def test_transaction_id(self, packet_details):
        i, _, _, _ = packet_details
        assert self.packet.struct.data[i].transaction.id == i

    def test_transaction_num_words(self, packet_details):
        i, _, _, _ = packet_details
        assert self.packet.struct.data[i].transaction.words == 0x1

    def test_transaction_info_code(self, packet_details):
        i, _, _, _ = packet_details
        assert self.packet.struct.data[i].transaction.info_code == 'REQUEST'

    def test_transaction_address(self, packet_details):
        i, type_id, address, _ = packet_details
        assert self.packet.struct.data[i].address == address

    def test_transaction_value(self, packet_details):
        i, type_id, _, value = packet_details
        # read transactions do not have a 'data' so should be None
        assert getattr(self.packet.struct.data[i], 'data', None) == value
