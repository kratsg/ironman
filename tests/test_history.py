from zope.interface.verify import verifyClass, verifyObject
from ironman.history import History
from ironman.interfaces import IHistory
from ironman.utilities import byteswap

from ironman.globals import IPBUS_VERSION, TESTPACKETS

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
