from ironman.utilities import chunks, byteswap

def test_chunks():
    assert list(chunks('abc', 1)) == ['a', 'b', 'c']
    assert list(chunks('abc', 2)) == ['ab', 'c']
    assert list(chunks('abc', 3)) == ['abc']

def test_byteswap():
    assert byteswap('\xf0\x00\x00 \x0f\x01\x00 \x03\x00\x00\x00') == ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'
