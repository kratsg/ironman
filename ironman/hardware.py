from zope.interface import implements
from ironman.interfaces import IHardwareManager, IHardwareMap

class HardwareManager(object):
    implements(IHardwareManager)
    pass

class HardwareMap(object):
    implements(IHardwareMap)
    pass
