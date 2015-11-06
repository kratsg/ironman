from ironman.constructs.ipbus import IPBusConstruct
from ironman.globals import TESTPACKETS
from construct import FieldError, ValidationError

import pytest

def test_parse_big_endian():
    IPBusConstruct.parse(TESTPACKETS['big-endian'])

def test_fail_parsing_little_endian():
    with pytest.raises(ValidationError) as e:
        IPBusConstruct.parse(TESTPACKETS['little-endian'])
    assert e.value.args == ('invalid object', 2)

@pytest.mark.parametrize("data", [TESTPACKETS['big-endian'][:i] for i in range(4)])
def test_bad_ipbus_packet_header(data):
    """ This test just runs over a technically valid, yet incomplete ipbus packet header
    """
    with pytest.raises(FieldError) as e:
        IPBusConstruct.parse(data)
