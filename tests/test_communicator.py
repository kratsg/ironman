from zope.interface.verify import verifyClass, verifyObject
from ironman.communicator import Jarvis
from ironman.interfaces import ICommunicationSlave

from ironman.hardware import HardwareManager

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
