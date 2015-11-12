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
    @pytest.fixture(autouse=True)
    def set_up(self):
        # this checks a simple communication that works
        class FakeManager:
            def parse_address(self, addr):
                return 'file'

        self.j = Jarvis()
        self.j.set_hardware_manager(FakeManager())

    def test_jarvis_create(self):
        assert self.j is not None

    def test_jarvis_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(ICommunicationSlave, Jarvis)

    def test_jarvis_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(ICommunicationSlave, self.j)

    def test_jarvis_packet(self, tmpdir):
        f = tmpdir.mkdir("sub").join("hello.txt")
        f.write_binary("helloworld")

        @self.j.register('file')
        class TestIO(SimpleIO):
            __f__ = f.strpath

        p = IPBusPacket(TESTPACKETS['big-endian'])
        self.j(p)

        self.j.unregister('file')

    def test_jarvis_no_read(self):
        with pytest.raises(AttributeError) as excinfo:
            @self.j.register('bad-method')
            class Bad(object):
                def write(self): pass
        assert "has no attribute 'read'" in str(excinfo.value)

    def test_jarvis_no_write(self):
        with pytest.raises(AttributeError) as excinfo:
            @self.j.register('bad-method')
            class Bad(object):
                def read(self): pass
        assert "has no attribute 'write'" in str(excinfo.value)

    def test_jarvis_ducktyping(self):
        @self.j.register('ok-method')
        class Ok(object):
            def read(self): pass
            def write(self): pass
        assert 1  # we should have no error
