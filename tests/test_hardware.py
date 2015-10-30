from zope.interface.verify import verifyClass, verifyObject
from ironman.hardware import HardwareManager, HardwareMap
from ironman.interfaces import IHardwareManager, IHardwareMap

class TestHardwareManager:
    def test_hardware_manager_create(self):
        obj = HardwareManager()
        assert obj is not None

    def test_hardware_manager_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(IHardwareManager, HardwareManager)

    def test_hardware_manager_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(IHardwareManager, HardwareManager())

class TestHardwareMap:
    def test_hardware_map_create(self):
        obj = HardwareMap()
        assert obj is not None

    def test_hardware_map_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(IHardwareMap, HardwareMap)

    def test_hardware_map_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(IHardwareMap, HardwareMap())
