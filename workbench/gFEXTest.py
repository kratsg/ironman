from ironman.hardware import HardwareManager, HardwareMap, HardwareNode
manager = HardwareManager()
manager.add(HardwareMap(file('xadc.xml').read(), 'xadc'))
