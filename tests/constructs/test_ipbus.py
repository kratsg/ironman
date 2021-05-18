from ironman.constructs.ipbus import IPBusConstruct, IPBusWords, PacketHeaderStruct, ControlHeaderStruct
from ironman.globals import TESTPACKETS
from construct import StreamError, ValidationError
import pytest

def test_parse_big_endian():
    IPBusConstruct.parse(TESTPACKETS['big-endian'])

def test_parse_little_endian():
    IPBusConstruct.parse(TESTPACKETS['little-endian'])

class TestIPBusPacketHeader:
    @pytest.mark.parametrize("data", [TESTPACKETS['big-endian'][:i] for i in range(PacketHeaderStruct.sizeof())])
    def test_bad_ipbus_packet_header(self, data):
        """ This test just runs over a technically valid, yet incomplete ipbus packet header
        """
        with pytest.raises(StreamError) as e:
            PacketHeaderStruct.parse(data)

    def test_bad_ipbus_version(self):
        with pytest.raises(ValidationError) as e:
            PacketHeaderStruct.parse(TESTPACKETS['wrong protocol version'])

class TestIPBusControlPacket:
    @pytest.mark.parametrize("data", [TESTPACKETS['big-endian'][PacketHeaderStruct.sizeof():i] for i in range(PacketHeaderStruct.sizeof(), ControlHeaderStruct.sizeof()+4)])
    def test_bad_control_packet_header(self, data):
        """ This test just runs over a technically valid, yet incomplete control transaction header
        """
        with pytest.raises(StreamError) as e:
            ControlHeaderStruct.parse(data)

def test_data_endianness_switch():
    data_big = bytearray.fromhex('200000f020000100deadbeef')
    packet = IPBusConstruct.parse(data_big)
    assert packet.endian == 'BIG'
    assert packet.transactions[0].data == [bytearray.fromhex('deadbeef')]

    packet.endian='LITTLE' # make it little-endian
    data_lil = IPBusConstruct.build(packet)
    assert data_lil == bytearray.fromhex('f000002000010020efbeadde')
    assert IPBusConstruct.parse(data_lil).endian == 'LITTLE'
    assert IPBusConstruct.parse(data_lil).transactions[0].data == [bytearray.fromhex('deadbeef')]


def test_packet_endian_equality():
    read_req_big = bytearray.fromhex('200000f02000010f00000003')
    read_res_big = bytearray.fromhex('200000f020000100deadbeef')

    read_req_lil = bytearray.fromhex('f00000200f01002003000000')
    read_res_lil = bytearray.fromhex('f000002000010020efbeadde')

    res_p_big = IPBusConstruct.parse(read_req_big)
    req_p_big = IPBusConstruct.parse(read_res_big)
    res_p_lil = IPBusConstruct.parse(read_req_lil)
    req_p_lil = IPBusConstruct.parse(read_res_lil)

    assert res_p_big.endian == 'BIG'
    assert res_p_lil.endian == 'LITTLE'
    assert res_p_big.status == res_p_lil.status
    assert res_p_big.resend == res_p_lil.resend
    assert res_p_big.transactions[0].address == res_p_lil.transactions[0].address
    assert res_p_big.transactions == res_p_lil.transactions

"""
foo = IPBusConstruct.parse(b'\x20\x00\x00\xf0\x20\x00\x01\x0f\x00\x00\x00\x03')
print foo
#print IPBusConstruct.build(foo).encode('hex')

#bar = IPBusConstruct.parse(b'\x20\x00\x00\xf0\x20\x00\x01\x1f\xac\x00\x10\xf4\x00\x00\x00\x01')
#print bar
#print IPBusConstruct.build(bar).encode('hex')

baz = IPBusConstruct.parse(b'\xf0\x00\x00\x20\x0f\x01\x00\x20\x03\x00\x00\x00')
print baz
"""
