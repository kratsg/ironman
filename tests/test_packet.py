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

class TestIPBusControlPacketParse:
    @pytest.fixture(autouse=True,
                    params=[BENDIAN_TESTPACKET, LENDIAN_TESTPACKET, COMPLEXCONTROL_TESTPACKET])
    def init_packet(self, request):
        self.packet = IPBusPacket(request.param)

    def test_protocol_version(self):
        assert self.packet.protocol_version == IPBUS_VERSION

    def test_header_reserved(self):
        assert self.packet.struct.header.reserved == 0x0

    def test_packet_id(self):
        assert self.packet.packet_id == 0x0

    def test_byteorder(self):
        assert self.packet.byteorder == 0xf

    def test_control_type(self):
        assert self.packet.packet_type == 'CONTROL'

    def test_packet_swap(self):
        swapped_packet = IPBusPacket(byteswap(self.packet.raw))
        assert self.packet.struct == swapped_packet.struct

class TestIPBusControlPacketSimpleParse:
    @pytest.fixture(autouse=True)
    def init_packet(self):
        self.packet = IPBusPacket(BENDIAN_TESTPACKET)

    def test_length(self):
        assert len(self.packet.struct.data) == 1

    @pytest.mark.parametrize("i,type_id", [(0, 'READ',)])
    def test_transaction_type_id(self, i, type_id):
        assert self.packet.struct.data[i].transaction.type_id == type_id

    @pytest.mark.parametrize("i", range(1))
    def test_transaction_id(self, i):
        assert self.packet.struct.data[i].transaction.id == i

    @pytest.mark.parametrize("i", range(1))
    def test_transaction_num_words(self, i):
        assert self.packet.struct.data[i].transaction.words == 0x1

    @pytest.mark.parametrize("i", range(1))
    def test_transaction_info_code(self, i):
        assert self.packet.struct.data[i].transaction.info_code == 'REQUEST'

class TestIPBusControlPacketComplexParse:
    @pytest.fixture(autouse=True)
    def init_packet(self):
        self.packet = IPBusPacket(COMPLEXCONTROL_TESTPACKET)

    def test_length(self):
        assert len(self.packet.struct.data) == 3

    @pytest.mark.parametrize("i,type_id", [(0, 'WRITE',), (1, 'WRITE', ), (2, 'READ', )])
    def test_transaction_type_id(self, i, type_id):
        assert self.packet.struct.data[i].transaction.type_id == type_id

    @pytest.mark.parametrize("i", range(3))
    def test_transaction_id(self, i):
        assert self.packet.struct.data[i].transaction.id == i

    @pytest.mark.parametrize("i", range(3))
    def test_transaction_num_words(self, i):
        assert self.packet.struct.data[i].transaction.words == 0x1

    @pytest.mark.parametrize("i", range(3))
    def test_transaction_info_code(self, i):
        assert self.packet.struct.data[i].transaction.info_code == 'REQUEST'

'''
More complicated packet example:
Handling Transaction
    ['1f010020', '06000000', '00000000']
    Handling Control Type: write
        Location: 00000006
        Value:  00000000
Handling Transaction
    ['1f010120', '06000000', '01000000']
    Handling Control Type: write
        Location: 00000006
        Value:  00000001
Handling Transaction
    ['0f010220', '03000000']
    Handling Control Type: read
        1 32-bit words from
        Location: 03000000
============================================================
|---------------------Outbound Message---------------------|
|    From: ('0.0.0.0', 8888)                               |
|    To  : ('128.135.152.116', 58367)                      |
|    Data                                                  |
|     |- Word 0    f0000020                                |
|     |- Word 1    10010020                                |
|     |- Word 2    10010120                                |
|     |- Word 3    00010220                                |
|     |- Word 4    01000000                                |
|                                                          |
============================================================
'''
