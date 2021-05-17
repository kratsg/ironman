import asyncore
import socket, time

# reference time
TIME1970 = 2208988800

class TimeChannel(asyncore.dispatcher):

    def handle_write(self):
        print("handle_write()")
        t = int(time.time()) + TIME1970
        t = chr(t>>24&255) + chr(t>>16&255) + chr(t>>8&255) + chr(t&255)
        self.send(t)
        self.close()

class TimeServer(asyncore.dispatcher):

    def __init__(self, port=8037):
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(5)
        print "listening on port", self.port

    def handle_accept(self):
        channel, addr = self.accept()
        TimeChannel(channel)

server = TimeServer(8037)
asyncore.loop()

