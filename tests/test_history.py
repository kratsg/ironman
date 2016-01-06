from zope.interface.verify import verifyClass, verifyObject
from ironman.history import History
from ironman.interfaces import IHistory
from ironman.utilities import byteswap

from ironman.globals import IPBUS_VERSION, TESTPACKETS
from ironman.packet import IPBusPacket

# fixtures for passing in the objects
import pytest

def test_history_create():
    obj = History()
    assert obj is not None

def test_history_class_iface():
    # Assure the class implements the declared interface
    assert verifyClass(IHistory, History)

def test_history_instance_iface():
    # Assure instances of the class provide the declared interface
    assert verifyObject(IHistory, History())

def test_history_empty():
    h = History()
    assert len(h) == 0
    assert any(h.packets) == False
    assert len(h.packets) == h.maxlen

def test_history_record():
    h = History()
    for i in range(101):
        p = IPBusPacket(TESTPACKETS['big-endian'])
        p.request.header.id = i
        h.record(p)
    assert len(h) == h.maxlen
    assert all(h.packets) == True
    assert 0 not in h
    assert 1 in h
    assert 100 in h
