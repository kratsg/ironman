from zope.interface.verify import verifyClass, verifyObject
from ironman.communicator import Jarvis, SimpleIO
from ironman.interfaces import ICommunicationSlave
from ironman.hardware import HardwareManager
from ironman.globals import TESTPACKETS
from ironman.packet import IPBusPacket
from twisted.internet.defer import inlineCallbacks, returnValue

import pytest

hwmanager = HardwareManager()

class TestJarvis:
    def test_jarvis_create(self):
        obj = Jarvis()
        assert obj is not None

    def test_jarvis_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(ICommunicationSlave, Jarvis)

    def test_jarvis_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(ICommunicationSlave, Jarvis())

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

class TestJarvisCommunication:
    @pytest.fixture(autouse=True)
    def set_up(self, tmpdir):
        self.j = Jarvis()
        self.j.set_hardware_manager(FakeManager())
        self.f = tmpdir.mkdir("sub").join("hello.txt")
        self.f.write_binary("helloworld")

        @self.j.register('file')
        class TestIO(SimpleIO):
            __f__ = self.f.strpath

    def test_jarvis_packet(self, tmpdir):
        p = IPBusPacket(TESTPACKETS['big-endian'])
        self.j(p)
