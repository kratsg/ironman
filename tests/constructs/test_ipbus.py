from ironman.constructs.ipbus import IPBusConstruct, PacketHeaderStruct, ControlHeaderStruct
from ironman.globals import TESTPACKETS
from construct import FieldError, ValidationError

import pytest

def test_parse_big_endian():
    IPBusConstruct.parse(TESTPACKETS['big-endian'])

def test_fail_parsing_little_endian():
    with pytest.raises(ValidationError) as e:
        IPBusConstruct.parse(TESTPACKETS['little-endian'])

class TestIPBusPacketHeader:
    @pytest.mark.parametrize("data", [TESTPACKETS['big-endian'][:i] for i in range(PacketHeaderStruct.sizeof())])
    def test_bad_ipbus_packet_header(self, data):
        """ This test just runs over a technically valid, yet incomplete ipbus packet header
        """
        with pytest.raises(FieldError) as e:
            PacketHeaderStruct.parse(data)

    def test_bad_ipbus_version(self):
        with pytest.raises(ValidationError) as e:
            PacketHeaderStruct.parse(TESTPACKETS['wrong protocol version'])

class TestIPBusControlPacket:
    @pytest.mark.parametrize("data", [TESTPACKETS['big-endian'][PacketHeaderStruct.sizeof():i] for i in range(PacketHeaderStruct.sizeof(), ControlHeaderStruct.sizeof()+4)])
    def test_bad_control_packet_header(self, data):
        """ This test just runs over a technically valid, yet incomplete control transaction header
        """
        with pytest.raises(FieldError) as e:
            ControlHeaderStruct.parse(data)
