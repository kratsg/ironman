IPBUS_VERSION = 2
TESTPACKETS = {
    'big-endian': b'\x20\x00\x00\xf0\x20\x00\x01\x0f\x00\x00\x00\x03',
    'little-endian': b'\xf0\x00\x00\x20\x0f\x01\x00\x20\x03\x00\x00\x00',
    'complex control': b'\xf0\x00\x00 \x1f\x01\x00 \x06\x00\x00\x00\x00\x00\x00\x00\x1f\x01\x01 \x06\x00\x00\x00\x01\x00\x00\x00\x0f\x01\x02 \x03\x00\x00\x00',
    'wrong protocol version': b'\x00\x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03',
    'read response': bytearray.fromhex('f000002000010020efbeadde'),
}

TESTRESPONSES = {
    'big-endian': b'\x20\x00\x00\xf0\x20\x00\x10\x00\x00\x00\x00\x01',
    'little-endian': b'\xf0\x00\x00\x20\x00\x01\x00\x20\x01\x00\x00\x00',
}
