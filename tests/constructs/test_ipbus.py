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
    in_data = '200000f020000100deadbeef'.decode('hex')
    packet = IPBusConstruct.parse(in_data)

    assert packet.endian == 'BIG'

    packet.endian='LITTLE' # make it little-endian
    out_data = IPBusConstruct.build(packet)
    assert out_data.encode('hex') == 'f000002000010020efbeadde'

    assert IPBusConstruct.parse(out_data).endian == 'LITTLE'

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
