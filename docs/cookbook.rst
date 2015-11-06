.. _ref-cookbook:

=========
Cookbook
=========

Handling IPBus packets
-----------------------------

It is common to use ironman to parse and build ipbus packets. Expecting this major usage of the software being written, we use `the awesome construct package <https://github.com/construct/construct/>`_ to build an :attr:`~ironman.constructs.ipbus.IPBusConstruct` builder/parser to make it easier for everyone to use.

In the examples that follow, we will use (and assume) a `big-endian` aligned data packet that contains the IPBus commands.

.. code-block:: python

    data = ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'

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
>>> data = ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'
>>> p = IPBusConstruct.parse(data)
>>> print p
Container:
    header = Container:
        protocol_version = 2
        reserved = 0
        id = 0
        byteorder = 15
        type_id = 'CONTROL'
    data = [
        Container:
            transaction = Container:
                protocol_version = 2
                id = 0
                words = 1
                type_id = 'READ'
                info_code = 'REQUEST'
            address = 3
    ]
>>>

Building an IPBus Packet
~~~~~~~~~~~~~~~~~~~~~~~~

Because of duck-typing, any object can make do when passing into the construct builder. See the `construct` docs for more information here. In this case, we will take the original packet which has a packet id :code:`0x0` in the header and update it to :code:`0x1`

>>> from ironman.constructs.ipbus import IPBusConstruct
>>> data = ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'
>>> p = IPBusConstruct.parse(data)
>>> p.header.packet_id = 0x1
>>> new_data = IPBusConstruct.build(p)
>>> print new_data.__repr__()
' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'
>>>

Note that when building an IPBus Packet, an error would be raised if we cannot build it. For example, if we tried to bump the protocol version to a non-valid one

>>> from ironman.constructs.ipbus import IPBusConstruct
>>> data = ' \x00\x00\xf0 \x00\x01\x0f\x00\x00\x00\x03'
>>> p = IPBusConstruct.parse(data)
>>> p.header.protocol_version = 0x0
>>> new_data = IPBusConstruct.build(p)
Traceback (most recent call last):
    ...
ValidationError: ('invalid object', 0)

which is letting us know (not a very verbose error) that the :code:`0x0` value is wrong.
