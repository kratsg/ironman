def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def byteswap(data, word_size=8):
    """ Swap the byte-ordering in a packet with N=8 bytes per word
    """
    return reduce(lambda x,y: x+''.join(reversed(y)), chunks(data, 4), '')

from construct import Construct
class PrintContext(Construct):
    def _parse(self, stream, context):
        print context
