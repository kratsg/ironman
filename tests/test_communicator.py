from zope.interface.verify import verifyClass, verifyObject
from ironman.communicator import Jarvis
from ironman.interfaces import ICommunicationSlave
from ironman.hardware import HardwareManager
from ironman.globals import TESTPACKETS
from ironman.constructs.ipbus import IPBusConstruct
from twisted.internet.defer import inlineCallbacks, returnValue

import pytest

hwmanager = HardwareManager()

class TestJarvis:
    def test_jarvis_create(self):
        obj = Jarvis(hwmanager)
        assert obj is not None

    def test_jarvis_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(ICommunicationSlave, Jarvis)

    def test_jarvis_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(ICommunicationSlave, Jarvis(hwmanager))

FileXML = \
"""<?xml version="1.0" encoding="ISO-8859-1"?>

<node id="TOP">
    <node id="ctrl_reg" address="0x0" description="ctrl/stat register">
        <node id="rst" address="0x0" permissions="3"/>
        <node id="id" address="0x1" permissions="3"/>
    </node>
</node>
"""

# this checks a simple communication that works
class FakeManager:
    def parse_address(self, addr):
        return 'file'

class SimpleIO(Jarvis):
    __route__ = 'file'
    __f__ = '/Users/kratsg/Desktop/SimpleIO'
    implements(ICommunicationProtocol)

    def read(self, offset, size):
        with open(self.__f__, 'rb') as f:
            f.seek(offset)
            return f.read(size)

    def write(self, offset, data):
        with open(self.__f__, 'r+b') as f:
            f.seek(offset)
            return f.write(data)

class TestJarvisCommunication:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.j = Jarvis()
        self.j.set_hardware_manager(FakeManager())

    def test_jarvis_packet():
        p = IPBusConstruct.parse(TESTPACKETS['big-endian'])
        j(p)
