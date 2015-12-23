from zope.interface.verify import verifyClass, verifyObject
from ironman.hardware import HardwareManager, HardwareMap, HardwareNode
from ironman.interfaces import IHardwareManager, IHardwareMap, IHardwareNode

import pytest

testYML = \
"""
nodes:
    -
        id: temperature
        address: 0x00000000
        nodes:
            - &offset {id: offset, address: 0x0, permissions: 1}
            - &raw {id: raw, address: 0x1, permissions: 1}
            - &scale {id: scale, address: 0x2, permissions: 1}
    -
        id: vccint
        address: 0x00000010
        nodes: [*raw, *scale]
    -
        id: vccaux
        address: 0x00000020
        nodes: [*raw, *scale]
    -
        id: vccbram
        address: 0x00000030
        nodes: [*raw, *scale]
    -
        id: vccpint
        address: 0x00000040
        nodes: [*raw, *scale]
    -
        id: vccpaux
        address: 0x00000050
        nodes: [*raw, *scale]
    -
        id: vccoddr
        address: 0x00000060
        nodes: [*raw, *scale]
    -
        id: vrefp
        address: 0x00000070
        nodes: [*raw, *scale]
    -
        id: vrefn
        address: 0x00000080
        nodes: [*raw, *scale]
"""

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
    @pytest.fixture(autouse=True)
    def init_map(self):
        self.hwmap = HardwareMap(testYML, 'test')

    def test_hardware_map_create(self):
        assert self.hwmap is not None

    def test_hardware_map_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(IHardwareMap, HardwareMap)

    def test_hardware_map_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(IHardwareMap, self.hwmap)

class TestHardwareNodeInterface:
    def test_hardware_node_create(self):
        obj = HardwareNode({'permissions': 2}, {})
        assert obj is not None

    def test_hardware_node_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(IHardwareNode, HardwareNode)

    def test_hardware_node_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(IHardwareNode, HardwareNode({}, {}))

class TestHardwareNode:
    @pytest.fixture(autouse=True, params=[
        {"permissions": 0, "readable": False, "writeable": False, "isOk": False},
        {"permissions": 1, "readable": True, "writeable": False, "isOk": True},
        {"permissions": 2, "readable": False, "writeable": True, "isOk": False},
        {"permissions": 3, "readable": True, "writeable": True, "isOk": True}
    ])
    def init_node(self, request):
        self.data = request.param
        self.node = HardwareNode(request.param, {})

    def test_permissions(self):
        assert self.node.permissions == self.data.get('permissions')

    def test_readable(self):
        assert self.node.readable == self.data.get('readable')

    def test_writeable(self):
        assert self.node.writeable == self.data.get('writeable')

    def test_not_ok(self):
        assert self.node.isOk == self.data.get('isOk')

    def test_hw_map(self):
        assert self.node.hw_map == {}
