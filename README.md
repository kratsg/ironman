```
pip install -r requirements.txt
```

# Tutorial

Since we will be predominantly using Twisted within the Zynq to manage the Reactor workflow ("callbacks"), I suggest reading through [this tutorial](http://krondo.com/?page_id=1327) on your own time to get up to speed on how it works and some details of sockets.

## To Do

- split udp and tcp into different, separate protocols: http://stackoverflow.com/questions/33224142/twisted-protocol-that-simultaneously-handles-tcp-and-udp-at-once

## Ideas

- make it like twisted.web - we build Request objects which need to find Resource objects that provide actions (maybe too complicated, try and simplify?) [link](http://twistedmatrix.com/trac/browser/trunk/twisted/web)

# Testing

```
tox
```
