def chunks(mylist, chunk_size):
    """Yield successive n-sized chunks from a list."""
    for i in range(0, len(mylist), chunk_size):
        yield mylist[i : i + chunk_size]


from construct import Construct


class PrintContext(Construct):
    def _parse(self, *args):
        _, context = args
        import pdb

        pdb.set_trace()
        print(context)

    def _build(self, *args):
        import pdb

        pdb.set_trace()
