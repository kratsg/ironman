.. _ref-cookbook:

=========
Cookbook
=========

Handling IPBus packets
-----------------------------

It is common to use ironman to parse and build ipbus packets. Expecting this major usage of the software being written, we use `the awesome construct package <https://github.com/construct/construct/>`_ to build an :attr:`~ironman.constructs.ipbus.IPBusConstruct` builder/parser to make it easier for everyone to use.

In the examples that follow, we will use (and assume) a `big-endian` aligned data packet that contains the IPBus commands.

.. code-block:: python

    data = '\x20\x00\x00\xf0\x20\x00\x01\x0f\x00\x00\x00\x03'

which is a single read transaction request from the `base address` :code:`0x3`. In particular, it contains three 32-bit words:

==== ============== =======================
Word Hex            Meaning
==== ============== =======================
0    ``0x200000f0`` IPBus Packet Header
1    ``0x200001f0`` Read Transaction Header
2    ``0x00000003`` Base Address of Read
==== ============== =======================

Parsing an IPBus Packet
~~~~~~~~~~~~~~~~~~~~~~~

>>> from ironman.constructs.ipbus import IPBusConstruct
>>> data = b'\x20\x00\x00\xf0\x20\x00\x01\x0f\x00\x00\x00\x03'
>>> p = IPBusConstruct.parse(data)
>>> print(p)
Container:
    endian = (enum) BIG 240
    header = Container:
        protocol_version = 2
        reserved = 0
        id = 0
        byteorder = 15
        type_id = (enum) CONTROL 0
    transactions = ListContainer:
        Container:
            header = Container:
                protocol_version = 2
                id = 0
                words = 1
                type_id = (enum) READ 0
                info_code = (enum) REQUEST 15
            address = 3
            data = None
    status = None
    resend = None

>>>

Building an IPBus Packet
~~~~~~~~~~~~~~~~~~~~~~~~

Because of duck-typing, any object can make do when passing into the construct builder. See the `construct` docs for more information here. In this case, we will take the original packet which has a packet id :code:`0x0` in the header and update it to :code:`0x1`

>>> from ironman.constructs.ipbus import IPBusConstruct
>>> data = b'\x20\x00\x00\xf0\x20\x00\x01\x0f\x00\x00\x00\x03'
>>> p = IPBusConstruct.parse(data)
>>> p.header.packet_id = 0x1
>>> new_data = IPBusConstruct.build(p)
>>> print(repr(new_data))
b' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'
>>>

Note that when building an IPBus Packet, an error would be raised if we cannot build it. For example, if we tried to bump the protocol version to a non-valid one

>>> from ironman.constructs.ipbus import IPBusConstruct
>>> data = b'\x20\x00\x00\xf0\x20\x00\x01\x0f\x00\x00\x00\x03'
>>> p = IPBusConstruct.parse(data)
>>> p.header.protocol_version = 0x0
>>> new_data = IPBusConstruct.build(p)
Traceback (most recent call last):
    ...
construct.core.ValidationError: object failed validation: 0


which is letting us know (not a very verbose error) that the :code:`0x0` value is wrong.

Creating a Response Packet
~~~~~~~~~~~~~~~~~~~~~~~~~~

As seen from the above examples, we have a read packet. Let's pretend the response is ``1234``. How do we build a response packet?

>>> from ironman.constructs.ipbus import IPBusConstruct
>>> in_data = b'\x20\x00\x00\xf0\x20\x00\x01\x0f\x00\x00\x00\x03'
>>> in_p = IPBusConstruct.parse(in_data)
>>> out_p = in_p
>>> out_p.transactions[0].data = [int(b"1234".hex(), 16)]
>>> out_data = IPBusConstruct.build(out_p)
Traceback (most recent call last):
    ...
construct.core.CheckError: check failed during building
>>> out_p.transactions[0].header.info_code = 'SUCCESS'
>>> out_data = IPBusConstruct.build(out_p)
>>> print(repr(out_data))
b' \x00\x00\xf0 \x00\x01\x001234'
>>>

and our work is done! Notice that it's not just a matter of setting the data field and building the packet.. we must also set the ``info_code`` field to a ``SUCCESS`` to signify that we're sending a *successful* response back.

Random Number Generator
-----------------------

One might like to be able to generate a full test of the ``ironman`` suite by setting up fake routes for reading/writing as a proof-of-concept. I demonstrate such a concept using a lot of different pieces of code here:

>>> from ironman.constructs.ipbus import IPBusConstruct, IPBusWords
>>> from ironman.hardware import HardwareManager, HardwareMap
>>> from ironman.communicator import Jarvis
>>> from ironman.packet import IPBusPacket
>>> from twisted.internet.defer import Deferred
>>> from ironman.constructs.ipbus import IPBusWord
>>> import random, struct
>>> random.seed(1)
>>>
>>> hardware_map = '''
... nodes:
...   -
...     id: random_number_generator
...     address: 0x00000000
...     nodes:
...       - {id: generate, address: 0x0, permissions: 1}
...       - {id: low_val, address: 0x1, permissions: 2}
...       - {id: high_val, address: 0x2, permissions: 2}
... '''
...
>>> j = Jarvis()
>>> manager = HardwareManager()
>>>
>>> manager.add(HardwareMap(hardware_map, 'main'))
>>> j.set_hardware_manager(manager)
>>>
>>> @j.register('main')
... class RandomNumberGeneratorController:
...   __low__  = 0
...   __high__ = 9
...   def generate(self):
...     return IPBusWord.build(random.randint(self.__class__.__low__, self.__class__.__high__))
...
...   def read(self, offset, size):
...     if offset == 0x0: return ''.join(self.generate() for i in range(size))
...     elif offset == 0x1: return IPBusWord.build(self.__class__.__low__)
...     elif offset == 0x2: return IPBusWord.build(self.__class__.__high__)
...
...   def write(self, offset, data):
...     if offset == 0x0: pass
...     elif offset == 0x1: self.__class__.__low__ = IPBusWord.parse(data[0])
...     elif offset == 0x2: self.__class__.__high__ = IPBusWord.parse(data[0])
...     return
...
>>> def buildResponsePacket(packet):
...     packet.response.transactions[0].header.info_code = 'SUCCESS'
...     return IPBusConstruct.build(packet.response)
...
>>> def printPacket(raw):
...    print("raw: {0:s}".format(repr(raw.hex())))
...    packet = IPBusConstruct.parse(raw)
...    print(packet)
...    print("data: {0:d}".format(struct.unpack('=I', IPBusWords.build(packet.transactions[0].data))[0]))
...
>>> d = Deferred().addCallback(IPBusPacket).addCallback(j).addCallback(buildResponsePacket).addCallback(printPacket)
>>> d.callback(bytearray.fromhex('200000f02000010f00000002'))  # read the upper limit
raw: '200000f02000010000000009'
Container:
    endian = (enum) BIG 240
    header = Container:
        protocol_version = 2
        reserved = 0
        id = 0
        byteorder = 15
        type_id = (enum) CONTROL 0
    transactions = ListContainer:
        Container:
            header = Container:
                protocol_version = 2
                id = 0
                words = 1
                type_id = (enum) READ 0
                info_code = (enum) SUCCESS 0
            address = None
            data = ListContainer:
                b'\x00\x00\x00\t'
    status = None
    resend = None
data: 9
