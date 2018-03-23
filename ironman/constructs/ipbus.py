from construct import Array, BitsInteger, BitStruct, Enum, GreedyRange, Struct, Int8ub, Int32ub, Int32ul, Int32sb, Int32sl, OneOf, Nibble, Octet, If, IfThenElse, ByteSwapped, this, Computed, Switch, Pointer, Check, Terminated
from ironman.globals import IPBUS_VERSION

PacketHeaderStruct = BitStruct(
                        "protocol_version" / OneOf(Nibble, [IPBUS_VERSION]),
                        "reserved" / OneOf(Nibble, [0x0]),
                        "id" / BitsInteger(16),
                        "byteorder" / OneOf(Nibble, [0xf]),
                        "type_id" / Enum(Nibble,
                          CONTROL = 0x0,
                          STATUS = 0x1,
                          RESEND = 0x2)
)
"""
Struct detailing the Packet Header logic

byteorder is `0xf` if big-endian and `0x0` if little-endian
"""

ControlHeaderStruct = BitStruct(
                         "protocol_version" / OneOf(Nibble, [IPBUS_VERSION]),
                         "id" / BitsInteger(12),
                         "words" / Octet,
                         "type_id" / Enum(Nibble,
                            READ = 0x0,
                            NOINCREAD = 0x2,
                            WRITE = 0x1,
                            NOINCWRITE = 0x3,
                            RMWBITS = 0x4,
                            RMWSUM = 0x5,
                            RCONFIG = 0x6,
                            WCONFIG = 0x7
                        ),
                        "info_code" / Enum(Nibble,
                            SUCCESS = 0x0,
                            BADHEADER = 0x1,
                            RBUSERROR = 0x4,
                            WBUSERROR = 0x5,
                            RBUSTIMEOUT = 0x6,
                            WBUSTIMEOUT = 0x7,
                            REQUEST = 0xf
                        )
)
"""
Struct detailing the Control Header logic
"""

ControlStruct = "ControlTransaction" / Struct(
                    "header" / IfThenElse(this._.bigendian, ControlHeaderStruct, ByteSwapped(ControlHeaderStruct)),
                    "address" / IfThenElse(this._.bigendian, Int32ub, Int32ul),
										"data" / Switch(lambda ctx: (ctx.header.type_id, ctx.header.info_code), {
											("READ","SUCCESS"): Array(this.header.words, IfThenElse(this._.bigendian, Int32ub, Int32ul)),
											("NOINCREAD","SUCCESS"): Array(this.header.words, IfThenElse(this._.bigendian, Int32ub, Int32ul)),
											("RCONFIG","SUCCESS"): Array(this.header.words, IfThenElse(this._.bigendian, Int32ub, Int32ul)),
                      ("WRITE","REQUEST"): Array(this.header.words, IfThenElse(this._.bigendian, Int32ub, Int32ul)),
                      ("NOINCWRITE","REQUEST"): Array(this.header.words, IfThenElse(this._.bigendian, Int32ub, Int32ul)),
                      ("WCONFIG","REQUEST"): Array(this.header.words, IfThenElse(this._.bigendian, Int32ub, Int32ul)),
                      ("RMWBITS", "REQUEST"): ["and" / IfThenElse(this._.bigendian, Int32ub, Int32ul), "or" / IfThenElse(this._.bigendian, Int32ub, Int32ul)],
                      ("RMWBITS", "SUCCESS"): IfThenElse(this._.bigendian, Int32ub, Int32ul),
                      ("RMWSUM", "REQUEST"): IfThenElse(this._.bigendian, Int32sb, Int32sl),  # note: signed 32-bit for subtraction!
                      ("RMWSUM", "SUCCESS"): IfThenElse(this._.bigendian, Int32ub, Int32ul)
										}, default=Check(lambda ctx: getattr(ctx, 'data', None) == None))
)

"""
Struct detailing the Control Action logic

.. note::

  - RMWBits: Should compute via :math:`X \Leftarrow (X\wedge A)\\vee (B\wedge(!A))`
  - RMWSum: Should compute via :math:`X \Leftarrow X+A`

"""

StatusRequestStruct = "StatusTransaction" / Struct("data" / Array(15, OneOf(Int32ub, [0])))
StatusResponseStruct = "StatusTransaction" / Struct("data" / Array(15, Int32ub))
"""
Struct detailing the Status Action logic
"""

ResendStruct = "ResendTransaction" / Struct()
"""
Struct detailing the Resend Action logic
"""

IPBusWords = "IPBusWords" / Struct("data" / GreedyRange(Int32ub))

IPBusConstruct = "IPBusPacket" / Struct(
                    "pointer" / Pointer(3, Int8ub),
                    "bigendian" / Computed(this.pointer == 0xf0),
                    "header" / IfThenElse(this.bigendian, PacketHeaderStruct, ByteSwapped(PacketHeaderStruct)),  # defined as 'header' in context

                    "transactions" / If(lambda ctx: ctx.header.type_id == "CONTROL", GreedyRange(ControlStruct)),
                    "status" / If(lambda ctx: ctx.header.type_id == "STATUS", StatusRequestStruct),
                    "resend" / If(lambda ctx: ctx.header.type_id == "RESEND", ResendStruct),
                    Terminated
)
"""
Top-level IPBus Construct which is a packet parser/builder
"""


