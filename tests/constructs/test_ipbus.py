from ironman.constructs.ipbus import IPBusConstruct
from ironman.globals import TESTPACKETS
from construct import ValidationError

import pytest

def test_parse_big_endian():
    IPBusConstruct.parse(TESTPACKETS['big-endian'])

def test_fail_parsing_little_endian():
    with pytest.raises(ValidationError) as e:
        IPBusConstruct.parse(TESTPACKETS['little-endian'])
    assert 'foo' == e.value


