from . import communicator
from . import hardware
from . import history
from . import interfaces
from . import packet
from . import server
from . import utilities
from .version import version as __version__

__all__ = [
    'communicator',
    'hardware',
    'history',
    'interfaces',
    'packet',
    'server',
    'utilities',
    '__version__',
]


def engage(proto='udp'):
    '''Fire thrusters.'''
    from .server import ServerFactory
    from twisted.internet import reactor
    from twisted.internet.defer import Deferred

    getattr(reactor, 'listen{:s}'.format(proto.upper()))(
        8888, ServerFactory(proto, Deferred)
    )
    reactor.run()
