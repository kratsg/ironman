import zope.interface.verify
from zope.interface.verify import verifyClass, verifyObject
from ironman.packet import IPBusPacket
from ironman.interfaces import IIPBusPacket
from construct import ListContainer

import array
from ironman.globals import IPBUS_VERSION, TESTPACKETS

# fixtures for passing in the objects
import pytest


@pytest.mark.parametrize(
    "data",
    [TESTPACKETS['big-endian'], TESTPACKETS['little-endian']],
    ids=["big-endian packet", "little-endian packet"],
)
def test_ipbus_packet_create(data):
    obj = IPBusPacket(data)
    assert obj is not None


def test_ipbus_packet_class_iface():
    # Assure the class implements the declared interface
    assert verifyClass(IIPBusPacket, IPBusPacket)


@pytest.mark.parametrize(
    "data",
    [TESTPACKETS['big-endian'], TESTPACKETS['little-endian']],
    ids=["big-endian packet", "little-endian packet"],
)
def test_ipbus_packet_instance_iface(data):
    # Assure instances of the class provide the declared interface
    assert verifyObject(IIPBusPacket, IPBusPacket(data))


class TestIPBusControlPacketParse:
    @pytest.fixture(
        autouse=True,
        params=[
            TESTPACKETS['big-endian'],
            TESTPACKETS['little-endian'],
            TESTPACKETS['complex control'],
            TESTPACKETS['read response'],
        ],
        ids=[
            "big-endian packet",
            "little-endian packet",
            "complex control packet",
            "read response packet",
        ],
    )
    def init_packet(self, request):
        self.packet = IPBusPacket(request.param)

    def test_protocol_version(self):
        assert self.packet.protocol_version == IPBUS_VERSION

    def test_header_reserved(self):
        assert self.packet.reserved == 0x0

    def test_packet_id(self):
        assert self.packet.packet_id == 0x0

    def test_byteorder(self):
        assert self.packet.byteorder == 0xF

    def test_control_type(self):
        assert self.packet.packet_type == 'CONTROL'

    def test_packet_swap(self):
        _raw = array.array("I", self.packet.raw)
        _raw.byteswap()
        swapped_raw = _raw.tobytes()
        swapped_packet = IPBusPacket(swapped_raw)
        assert self.packet.request.endian != swapped_packet.request.endian
        assert self.packet.request.transactions == swapped_packet.request.transactions


class TestIPBusControlPacketSimpleParse:
    @pytest.fixture(autouse=True)
    def init_packet(self):
        self.packet = IPBusPacket(TESTPACKETS['big-endian'])

    def test_length(self):
        assert len(self.packet.request.transactions) == 1

    # specify details about inside packets
    @pytest.fixture(
        params=[
            (
                0,
                'READ',
            )
        ],
        ids=["first"],
    )
    def packet_details(self, request):
        return request.param

    def test_transaction_type_id(self, packet_details):
        i, type_id = packet_details
        assert self.packet.request.transactions[i].header.type_id == type_id

    def test_transaction_id(self, packet_details):
        i, _ = packet_details
        assert self.packet.request.transactions[i].header.id == i

    def test_transaction_num_words(self, packet_details):
        i, _ = packet_details
        assert self.packet.request.transactions[i].header.words == 0x1

    def test_transaction_info_code(self, packet_details):
        i, _ = packet_details
        assert self.packet.request.transactions[i].header.info_code == 'REQUEST'


class TestIPBusControlPacketComplexParse:
    @pytest.fixture(autouse=True)
    def init_packet(self):
        self.packet = IPBusPacket(TESTPACKETS['complex control'])

    def test_length(self):
        assert len(self.packet.request.transactions) == 3

    @pytest.fixture(
        params=[
            (0, 'WRITE', 0x6, ListContainer([b'\x00\x00\x00\x00'])),
            (1, 'WRITE', 0x6, ListContainer([b'\x00\x00\x00\x01'])),
            (2, 'READ', 0x3, None),
        ],
        ids=["first", "second", "third"],
    )
    def packet_details(self, request):
        return request.param

    def test_transaction_type_id(self, packet_details):
        i, type_id, _, _ = packet_details
        assert self.packet.request.transactions[i].header.type_id == type_id

    def test_transaction_id(self, packet_details):
        i, _, _, _ = packet_details
        assert self.packet.request.transactions[i].header.id == i

    def test_transaction_num_words(self, packet_details):
        i, _, _, _ = packet_details
        assert self.packet.request.transactions[i].header.words == 0x1

    def test_transaction_info_code(self, packet_details):
        i, _, _, _ = packet_details
        assert self.packet.request.transactions[i].header.info_code == 'REQUEST'

    def test_transaction_address(self, packet_details):
        i, type_id, address, _ = packet_details
        assert self.packet.request.transactions[i].address == address

    def test_transaction_value(self, packet_details):
        i, type_id, _, value = packet_details
        # read transactions do not have a 'data' so should be None
        assert getattr(self.packet.request.transactions[i], 'data', None) == value
