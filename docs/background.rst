Background and Goals
====================

Ironman is a software infrastructure that will standardize communication protocols on chips with embedded processors. In particular, this was written for use in L1Calo with IPBus, but was written to maintain modularity and flexibility to evolve with changing needs.

We make it as easy as possible for *anyone* to put their pieces in to the general framework while maintaining the overall procedure. This software will

    - provide a wide array of standard networking protocols for reading and writing packets
    - allow for implementation of **custom communication protocols** for reading and writing the various hardware components
    - allow for definition of **custom hardware maps** which specify the layout of the entire board
    - use a single-threaded **reactor** model, an event-driven model, which is a global loop that fires listeners when certain events have triggered


