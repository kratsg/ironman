def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def byteswap(data, word_size=4):
    """ Swap the byte-ordering in a packet with N=4 bytes per word
    """
    return reduce(lambda x,y: x+''.join(reversed(y)), chunks(data, word_size), '')

from construct import Construct
class PrintContext(Construct):
    def _parse(self, *args):
        _, context = args
        import pdb; pdb.set_trace()
        print context

    def _build(self, *args):
        import pdb; pdb.set_trace()
