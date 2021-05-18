from .version import version as __version__
__all__ = ['communicator',
           'hardware',
           'history',
           'interfaces',
           'packet',
           'server',
           'utilities']

def engage(proto='udp'):
    ''' Fire thrusters.
    '''
    from ironman.server import ServerFactory
    from twisted.internet import reactor
    from twisted.internet.defer import Deferred
    getattr(reactor, 'listen{:s}'.format(proto.upper()))(8888, ServerFactory(proto, Deferred))
    reactor.run()
