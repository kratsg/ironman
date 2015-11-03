from construct import Array, BitField, BitStruct, Embed, Enum, GreedyRange, Struct, Switch, UBInt32, SBInt32

# define headers for ipbus packets
PacketHeaderStruct = BitStruct("header",
                        BitField("protocol_version", 4),
                        BitField("reserved", 4),
                        BitField("id", 16),
                        BitField("byteorder", 4),
                        Enum(BitField("type_id", 4),
                            CONTROL = 0x0,
                            STATUS = 0x1,
                            RESEND = 0x2
                        )
)

ControlHeaderStruct = BitStruct("transaction",
                        BitField("protocol_version", 4),
                        BitField("id", 12),
                        BitField("words", 8),
                        Enum(BitField("type_id", 4),
                            READ = 0x0,
                            NOINCREAD = 0x2,
                            WRITE = 0x1,
                            NOINCWRITE = 0x3,
                            RMWBITS = 0x4,
                            RMWSUM = 0x5,
                            RCONFIG = 0x6,
                            WCONFIG = 0x7
                        ),
                        Enum(BitField("info_code", 4),
                            SUCCESS = 0x0,
                            BADHEADER = 0x1,
                            RBUSERROR = 0x4,
                            WBUSERROR = 0x5,
                            RBUSTIMEOUT = 0x6,
                            WBUSTIMEOUT = 0x7,
                            REQUEST = 0xf
                        )
)

ReadStruct = Struct("read")

WriteStruct = Struct("write",
                Array(lambda ctx: ctx.words, UBInt32("data"))
)

""" X <= (X&A)|(B&(~A)) """
RMWBitsStruct = Struct("rmwbits",
                    UBInt32("and"),
                    UBInt32("or")
)

""" X<= X+A """
RMWSumStruct = Struct("rmwsum",
                SBInt32("addend")  # note: signed 32-bit for subtraction!
)

ControlStruct = Struct("ControlTransaction",
                    ControlHeaderStruct,
                    UBInt32("address"),
                    Embed(Switch("data", lambda ctx: ctx.transaction.type_id,
                        {
                            "READ": ReadStruct,
                            "NOINCREAD": ReadStruct,
                            "WRITE": WriteStruct,
                            "NOINCWRITE": WriteStruct,
                            "RMWBITS": RMWBitsStruct,
                            "RMWSUM": RMWSumStruct,
                            "RCONFIG": ReadStruct,
                            "WCONFIG": WriteStruct
                        }
                    ))
)

StatusStruct = Struct("StatusTransaction", Array(15, UBInt32("data")))

ResendStruct = Struct("ResendTransaction")

IPBusConstruct = Struct("IPBusPacket",
                    PacketHeaderStruct,  # defined as 'header' in context
                    Switch("data", lambda ctx: ctx.header.type_id,
                        {
                            "CONTROL" : GreedyRange(ControlStruct),
                            "STATUS" : StatusStruct,
                            "RESEND" : ResendStruct,
                        }
                    )
)
