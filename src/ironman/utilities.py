from functools import reduce

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

from construct import Construct
class PrintContext(Construct):
    def _parse(self, *args):
        _, context = args
        import pdb; pdb.set_trace()
        print(context)

    def _build(self, *args):
        import pdb; pdb.set_trace()
