from construct import (
    Array,
    BitsInteger,
    BitStruct,
    Enum,
    GreedyRange,
    Struct,
    OneOf,
    Nibble,
    Octet,
    If,
    IfThenElse,
    Bytes,
    ByteSwapped,
    this,
    Switch,
    Pointer,
    Check,
    Terminated,
    Int8ub,
    Int32ub,
    Int32ul,
)
from ..globals import IPBUS_VERSION
import sys

# internal _IPBusWord used inside of structs that depend on IPBusConstruct context for switching
#_IPBusWord = IfThenElse(this._.endian == 'BIG', Bytes(4), ByteSwapped(Bytes(4)))
_IPBusWord = IfThenElse(this._.endian != 'LITTLE', Bytes(4), ByteSwapped(Bytes(4))) # ECC - modify to work with status packets
IPBusWord = Bytes(4) if sys.byteorder == 'big' else ByteSwapped(Bytes(4))
IPBusWords = GreedyRange(IPBusWord)

# ECC - need to handle two words for RMWBITS
_IPBusWord_long = IfThenElse(this._.endian != 'LITTLE', Bytes(8), ByteSwapped(Bytes(8)))
IPBusWord_long = Bytes(8) if sys.byteorder == 'big' else ByteSwapped(Bytes(8))
IPBusWords_long = GreedyRange(IPBusWord_long)

''' This works
_IPBusWord_long = Bytes(8)
IPBusWord_long = Bytes(8) 
IPBusWords_long = GreedyRange(IPBusWord_long)
'''


PacketHeaderStruct = BitStruct(
    "protocol_version" / OneOf(Nibble, [IPBUS_VERSION]), 
    "reserved" / OneOf(Nibble, [0x0]), 
    "id" / BitsInteger(16),
    "byteorder" / OneOf(Nibble, [0xF]), 
    "type_id" / Enum(Nibble, CONTROL=0x0, STATUS=0x1, RESEND=0x2),
)

"""
Struct detailing the Packet Header logic

byteorder is `0xf` if big-endian and `0x0` if little-endian
"""

ControlHeaderStruct = BitStruct(
    "protocol_version" / OneOf(Nibble, [IPBUS_VERSION]),
    "id" / BitsInteger(12),
    "words" / Octet,
    "type_id"
    / Enum(
        Nibble,
        READ=0x0,
        NOINCREAD=0x2,
        WRITE=0x1,
        NOINCWRITE=0x3,
        RMWBITS=0x4,
        RMWSUM=0x5,
        RCONFIG=0x6,
        WCONFIG=0x7,
    ),
    "info_code"
    / Enum(
        Nibble,
        SUCCESS=0x0,
        BADHEADER=0x1,
        RBUSERROR=0x4,
        WBUSERROR=0x5,
        RBUSTIMEOUT=0x6,
        WBUSTIMEOUT=0x7,
        REQUEST=0xF,
    ),
)
"""
Struct detailing the Control Header logic
"""

ControlStruct = "ControlTransaction" / Struct(
    "header"
    / IfThenElse(
        this._.endian == 'BIG', ControlHeaderStruct, ByteSwapped(ControlHeaderStruct)
    ),
    "address"
    / If(
        this.header.info_code == "REQUEST",
        IfThenElse(this._.endian == 'BIG', Int32ub, Int32ul),
    ),
    "data"
    / Switch(
        lambda ctx: (ctx.header.type_id, ctx.header.info_code),
        {
            ("READ", "SUCCESS"): Array(this.header.words, _IPBusWord),
            ("NOINCREAD", "SUCCESS"): Array(this.header.words, _IPBusWord),
            ("RCONFIG", "SUCCESS"): Array(this.header.words, _IPBusWord),
            ("WRITE", "REQUEST"): Array(this.header.words, _IPBusWord),
            ("NOINCWRITE", "REQUEST"): Array(this.header.words, _IPBusWord),
            ("WCONFIG", "REQUEST"): Array(this.header.words, _IPBusWord),
            #("RMWBITS", "REQUEST"): ["and" / _IPBusWord, "or" / _IPBusWord],
            ("RMWBITS", "REQUEST"): Array(this.header.words, _IPBusWord_long), # ECC - unpack two words instead of one for RMWBITS
            ("RMWBITS", "SUCCESS"): _IPBusWord,
            ("RMWSUM", "REQUEST"): _IPBusWord,  # note: signed 32-bit for subtraction!
            ("RMWSUM", "SUCCESS"): _IPBusWord,
        },
        default=Check(lambda ctx: getattr(ctx, 'data', None) is None),
    ),
)

"""
Struct detailing the Control Action logic

.. note::

  - RMWBits: Should compute via :math:`X \\Leftarrow (X\\wedge A)\\vee (B\\wedge(!A))`
  - RMWSum: Should compute via :math:`X \\Leftarrow X+A`

"""

StatusRequestStruct = "StatusTransaction" / Struct(
    #"data" / Array(15, OneOf(_IPBusWord, [0]))
    "data" / Array(15, _IPBusWord) # ECC - status words shouldn't be just zeros
)
StatusResponseStruct = "StatusTransaction" / Struct("data" / Array(15, _IPBusWord))
"""
Struct detailing the Status Action logic
"""

ResendStruct = "ResendTransaction" / Struct()
"""
Struct detailing the Resend Action logic
"""

IPBusConstruct = "IPBusPacket" / Struct(
    ###"endian" / Enum(Pointer(3, Int8ub), BIG=0xF0, LITTLE=0x20), 
    "endian" / Enum(Pointer(3, Int8ub), BIG=0xF0, LITTLE=0x20, STAT=0xF1), # ECC - handle status words
    "header"
    / IfThenElse(
       #this.endian == 'BIG', PacketHeaderStruct, ByteSwapped(PacketHeaderStruct)
       this.endian != 'LITTLE', PacketHeaderStruct, ByteSwapped(PacketHeaderStruct) # ECC - to deal with status word
    ),  # defined as 'header' in context
    "transactions" / If(this.header.type_id == "CONTROL", GreedyRange(ControlStruct)),
    "status" / If(this.header.type_id == "STATUS", StatusRequestStruct),
    "resend" / If(this.header.type_id == "RESEND", ResendStruct),
    Terminated,
)
"""
Top-level IPBus Construct which is a packet parser/builder
"""
