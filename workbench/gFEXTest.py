from ironman.hardware import HardwareManager, HardwareMap, HardwareNode
manager = HardwareManager()
manager.add(HardwareMap(file('xadc.xml').read(), 'xadc'))

from ironman.communicator import Jarvis, ComplexIO
j = Jarvis()
j.set_hardware_manager(manager)

'''
root@zc706-zynq7:~# ls /sys/devices/soc0/amba@0/f8007100.ps7-xadc/iio\:device0/
dev                        in_voltage2_vccbram_raw    in_voltage6_vrefp_scale
events                     in_voltage2_vccbram_scale  in_voltage7_vrefn_raw
in_temp0_offset            in_voltage3_vccpint_raw    in_voltage7_vrefn_scale
in_temp0_raw               in_voltage3_vccpint_scale  name
in_temp0_scale             in_voltage4_vccpaux_raw    power
in_voltage0_vccint_raw     in_voltage4_vccpaux_scale  sampling_frequency
in_voltage0_vccint_scale   in_voltage5_vccoddr_raw    subsystem
in_voltage1_vccaux_raw     in_voltage5_vccoddr_scale  uevent
in_voltage1_vccaux_scale   in_voltage6_vrefp_raw
'''

@j.register('xadc')
class XADCController(ComplexIO):
    __base__ = "/sys/devices/soc0/amba@0/f8007100.ps7-xadc/iio:device0/"
    __f__ = {
                0:   __base__+"in_temp0_offset",
                1:   __base__+"in_temp0_raw",
                2:   __base__+"in_temp0_scale",
                17:  __base__+"in_voltage0_vccint_raw",
                18:  __base__+"in_voltage0_vccint_scale",
                33:  __base__+"in_voltage1_vccaux_raw",
                34:  __base__+"in_voltage1_vccaux_scale",
                49:  __base__+"in_voltage2_vccbram_raw",
                50:  __base__+"in_voltage2_vccbram_scale",
                65:  __base__+"in_voltage3_vccpint_raw",
                66:  __base__+"in_voltage3_vccpint_scale",
                81:  __base__+"in_voltage4_vccpaux_raw",
                82:  __base__+"in_voltage4_vccpaux_scale",
                97:  __base__+"in_voltage5_vccoddr_raw",
                98:  __base__+"in_voltage5_vccoddr_scale",
                113: __base__+"in_voltage6_vrefp_raw",
                114: __base__+"in_voltage6_vrefp_scale",
                129: __base__+"in_voltage7_vrefn_raw",
                130: __base__+"in_voltage7_vrefn_scale"
            }

from ironman.constructs.ipbus import PacketHeaderStruct, ControlHeaderStruct
def buildResponsePacket(packet):
    data = ''
    data += PacketHeaderStruct.build(packet.struct)
    for transaction, response in zip(packet.struct.data, packet.response):
        data += ControlHeaderStruct.build(transaction)
        data += response.encode("hex")
    return data


from ironman.server import ServerFactory
from ironman.packet import IPBusPacket
from twisted.internet import reactor
from twisted.internet.defer import Deferred

reactor.listenUDP(8888, ServerFactory('udp', lambda: Deferred().addCallback(IPBusPacket).addCallback(j).addCallback(buildResponsePacket)))
reactor.run()
