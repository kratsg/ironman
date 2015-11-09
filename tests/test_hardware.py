from zope.interface.verify import verifyClass, verifyObject
from ironman.hardware import HardwareManager, HardwareMap, HardwareNode
from ironman.interfaces import IHardwareManager, IHardwareMap, IHardwareNode

import pytest

testXML = \
"""<?xml version="1.0" encoding="ISO-8859-1"?>

<node id="TOP">
    <node id="ctrl_reg" address="0x0" description="ctrl/stat register">
        <node id="rst" address="0x0" permissions="3"/>
        <node id="id" address="0x1" permissions="3"/>
    </node>
    <node id="reg" address="0x2" description="read-write register">
        <node id="test" address="0x1" permissions="3"/>
    </node>
    <node id="ram" address="0x1000" mode="block" size="0x400" description="1kword RAM" permissions="3"/>
    <node id="err_inject" address="0x4" description="error injection ctrl/stat">
        <node id="rx_ctrl" address="0x0" permissions="3"/>
        <node id="tx_ctrl" address="0x1" permissions="3"/>
        <node id="rx_stat" address="0x2" permissions="3"/>
        <node id="tx_stat" address="0x3" permissions="3"/>
    </node>
    <node id="pram" address="0x2000" description="1kword peephole RAM">
        <node id="addr" address="0x0" permissions="3"/>
        <node id="data" mode="port" size="0x400" address="0x1"/>
    </node>
    <node id="pkt_ctr" address="0x8" description="packet counters">
        <node id="w_count" address="0x0" permissions="3"/>
        <node id="r_count" address="0x1" permissions="3"/>
    </node>
</node>
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
        self.hwmap = HardwareMap(testXML)

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
        obj = HardwareNode({'@permissions': 2})
        assert obj is not None

    def test_hardware_node_class_iface(self):
        # Assure the class implements the declared interface
        assert verifyClass(IHardwareNode, HardwareNode)

    def test_hardware_node_instance_iface(self):
        # Assure instances of the class provide the declared interface
        assert verifyObject(IHardwareNode, HardwareNode({}))

class TestHardwareNode:
    @pytest.fixture(autouse=True, params=[
        {"@permissions": 0, "readable": False, "writeable": False, "isOk": False},
        {"@permissions": 1, "readable": True, "writeable": False, "isOk": True},
        {"@permissions": 2, "readable": False, "writeable": True, "isOk": False},
        {"@permissions": 3, "readable": True, "writeable": True, "isOk": True}
    ])
    def init_node(self, request):
        self.data = request.param
        self.node = HardwareNode(request.param)

    def test_permissions(self):
        assert self.node.permissions == self.data.get('@permissions')

    def test_readable(self):
        assert self.node.readable == self.data.get('readable')

    def test_writeable(self):
        assert self.node.writeable == self.data.get('writeable')

    def test_not_ok(self):
        assert self.node.isOk == self.data.get('isOk')
