Background
==========

Ironman is a software infrastructure that will standardize communication protocols on chips with embedded processors. In particular, this was written for use in L1Calo with IPBus, but was written to maintain modularity and flexibility to evolve with changing needs.

To explain this approach, we first started with our vision for the software with an overview. Below, we explain each part in more detail.

Goals
-----

We make it as easy as possible for *anyone* to put their pieces in to the general framework while maintaining the overall procedure. This software will

    - provide a **wide array of standard networking protocols** for reading and writing packets
    - allow for implementation of **custom communication protocols** for reading and writing the various hardware components
    - allow for definition of **custom hardware maps** which specify the layout of the entire board
    - use a single-threaded **reactor** model, an event-driven model, which is a global loop that fires listeners when certain events have triggered


Overview
--------

.. image:: images/ironman.diagram.overview.png

An external client, such as a human or a monkey, is tasked with the job of communicating a transaction request or a status query of a piece of hardware (*ATLAS Client*). This is sent, for example, as an IPBus command to the board running **ironman** software. This request is received by a server actively listening and then dispatches this request to the System-on-Chip client. The System-on-Chip client is made self-aware using hardware definitions and dispatches this request along a callback chain to the Internal Communications Interface. It is at this point that the software handles the customized communication to fulfill the request of the biological being controling the ATLAS Client. After this, the response is formed, transferred back to the server who will transmit the information back to the client.

Server
~~~~~~

.. image:: images/ironman.diagram.server.png

The server has a few jobs to do upon receipt of a packet. As the server is actively listening, it is going to plug itself into the reactor and kick off the callback chain for us (known as *deferreds* or *promises*).

The server knows the format of the packet entirely and will unpack the data into a Request Packet Object that will be used by the rest of the software. It is at this point that a few checks are done, such as checking that the data *can* be unpacked as well as making sure the headers are valid.

If the basic sanity checks look good, then it must decide what to do with the packet. If the request requires communication with the hardware, then it will pass along the packet to the SoC Client to dispatch the request. If it simply requires information about the history of packets sent (such as a Resend Packet), then it will return the packets it records in history.

This leads to the other part of the server which is to maintain a log of all inbound/request and outbound/response packets. It is at this point which the board communicates with the outside world and makes it a suitable place to implement the history recording.

For those who are more familiar or learn better with some code:

>>> # grab pieces of ironman
>>> from ironman.server import ServerFactory
>>> from ironman.packet import IPBusPacket
>>> from ironman.history import History
>>> history = History()
>>>
>>> # we need deferreds and reactor from twisted
>>> from twisted.internet import reactor
>>> from twisted.internet.defer import Deferred
>>>
>>> # build up our callback chain
>>> def callbacks():
...    return Deferred().addCallback(IPBusPacket).addCallback(history.record)
>>>
>>> # listen for IPBus packets over UDP at port 8888
>>> reactor.listenUDP(8888, ServerFactory('udp', callbacks))
<ironman.server.UDP on 8888>
>>>
>>> # listen for IPBus packets over TCP at port 8889
>>> reactor.listenTCP(8889, ServerFactory('tcp', callbacks))
<<class 'twisted.internet.tcp.Port'> of ironman.server.TCPFactory on 8889>

and of course, this is all building up our logic. To actually start up the server, we simply need::

    # start the global loop
    reactor.run()

Notice how that independent of which transport is being used to communicate with the server, the same callback chain is being executed correctly.

Hardware Interface
~~~~~~~~~~~~~~~~~~

.. image:: images/ironman.diagram.hardware_interface.png

The job of the Hardware Interface is to parse the hardware definitions transferred to the board and build up a cached, global mapping of address to properties about the address. In Python terminology, this is a giant dictionary. It must assess that a single address is not taken up by two different hardware definitions (no conflicts) and that the hardware map is parseable and valid (the latter has yet to be defined yet). It will also provide a way to compute the checksum of the hardware map files to ensure that the board is running on the same definitions that the monkey has communicated to the board with.

The Hardware Manager is our primary means of interfacing. We can demonstrate via another code example:

>>> xadcyml = """ nodes:
...    -
...        id: temperature
...        address: 0x00000000
...        nodes:
...            - &offset {id: offset, address: 0x0, permissions: 1}
...            - &raw {id: raw, address: 0x1, permissions: 1}
...            - &scale {id: scale, address: 0x2, permissions: 1}
...    -
...        id: vccint
...        address: 0x00000010
...        nodes: [*raw, *scale]
...    -
...        id: vccaux
...        address: 0x00000020
...        nodes: [*raw, *scale]
...    -
...        id: vccbram
...        address: 0x00000030
...        nodes: [*raw, *scale]
...    -
...        id: vccpint
...        address: 0x00000040
...        nodes: [*raw, *scale]
...    -
...        id: vccpaux
...        address: 0x00000050
...        nodes: [*raw, *scale]
...    -
...        id: vccoddr
...        address: 0x00000060
...        nodes: [*raw, *scale]
...    -
...        id: vrefp
...        address: 0x00000070
...        nodes: [*raw, *scale]
...    -
...        id: vrefn
...        address: 0x00000080
...        nodes: [*raw, *scale]"""
>>>
>>> # initialize a manager to use for everyone that needs it
>>> from ironman.hardware import HardwareManager, HardwareMap
>>> manager = HardwareManager()
>>> # add a map to the manager
>>> manager.add(HardwareMap(xadcyml, 'xadc'))

Client
~~~~~~

.. image:: images/ironman.diagram.client.png

The job of the client here is to analyze the packet more thoroughly. If the client is handling the packet, then it must be a request packet. It will then communicate with the Hardware Interface to determine whether or not the transaction packet is good: valid address, valid permissions, valid data. If all of these things pass, it then passes the packet along to the Internal Communications which will build up a response.

It should be noted that the client is not allowed to modify the response packet at all. Only the Server and the Internal Communications are allowed to do this.

In **ironman**, the client is known as Jarvis (the assistant, get it?). Jarvis is used like so:

>>> # now let's make jarvis
>>> from ironman.communicator import Jarvis, ComplexIO
>>> jarvis = Jarvis()
>>> # tell Jarvis about our hardware manager
>>> jarvis.set_hardware_manager(manager)

In particular, Jarvis is one of the easiest things to set up since it contains a lot of internal logic to route requests appropriately and execute controllers for you. In this way, Jarvis is a lot like a *router*.

Internal Communications
~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/ironman.diagram.communications.png

Lastly, the Internal Communications is primarily custom code written by the developers to do exactly that: communicate with the board. Depending on how the board is set up, there may be a virtual filesystem or raw pointers or custom drivers that the code will need to access. Since this is something that will vary on a board-by-board basis, we leave most of this code up to the user and only provide a few simple cases for file reading and writing.

Continuing on with our code examples as above, you might have your driver create a virtual file system for the temperature. So how would you create a custom communications controller that Jarvis knows about that handles the requests?

>>> # register a controller with jarvis
>>> @jarvis.register('xadc')
... class XADCController(ComplexIO):
...     __base__ = "/sys/devices/soc0/amba@0/f8007100.ps7-xadc/iio:device0/"
...     __f__ = {
...                 0:   __base__+"in_temp0_offset",
...                 1:   __base__+"in_temp0_raw",
...                 2:   __base__+"in_temp0_scale",
...                 17:  __base__+"in_voltage0_vccint_raw",
...                 18:  __base__+"in_voltage0_vccint_scale",
...                 33:  __base__+"in_voltage1_vccaux_raw",
...                 34:  __base__+"in_voltage1_vccaux_scale",
...                 49:  __base__+"in_voltage2_vccbram_raw",
...                 50:  __base__+"in_voltage2_vccbram_scale",
...                 65:  __base__+"in_voltage3_vccpint_raw",
...                 66:  __base__+"in_voltage3_vccpint_scale",
...                 81:  __base__+"in_voltage4_vccpaux_raw",
...                 82:  __base__+"in_voltage4_vccpaux_scale",
...                 97:  __base__+"in_voltage5_vccoddr_raw",
...                 98:  __base__+"in_voltage5_vccoddr_scale",
...                 113: __base__+"in_voltage6_vrefp_raw",
...                 114: __base__+"in_voltage6_vrefp_scale",
...                 129: __base__+"in_voltage7_vrefn_raw",
...                 130: __base__+"in_voltage7_vrefn_scale"
...             }

And you are done. This will read from :code:`/sys/devices/soc0/amba@0/f8007100.ps7-xadc/iio:device0/in_temp0_offset` if an IPBus read request is recieved for address :code:`0x0`. Similarly, it will read from ``in_voltage6_vrefp_raw`` if the address is ``0x71`` (which is ``113`` in decimal).

In this particular example, it is assumed you had added a hardware definitions for the *xADC* controller which is being registered to Jarvis. Each file path is associated with an address that you would explicitly map out. A future iteration of how hardware gets defined should alleviate the numerous redefinitions of addresses that occur.

