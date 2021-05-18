from ironman.utilities import chunks

def test_chunks():
    assert list(chunks('abc', 1)) == ['a', 'b', 'c']
    assert list(chunks('abc', 2)) == ['ab', 'c']
    assert list(chunks('abc', 3)) == ['abc']
