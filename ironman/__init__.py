__version__ = '0.1.1'
__all__ = ['communicator',
           'hardware',
           'interfaces',
           'packet',
           'server',
           'utilities']

def engage():
    ''' Fire thrusters.
    '''
    from ironman.server import IPBusServerProtocol
    from twisted.internet import reactor
    from twisted.internet.defer import Deferred
    reactor.listenUDP(8888, IPBusServerProtocol(Deferred))
    reactor.run()
