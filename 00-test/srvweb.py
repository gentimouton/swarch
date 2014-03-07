import socket
from time import sleep

# HOST = 'localhost'                 # Symbolic name meaning all available interfaces
# PORT = 8888              # Arbitrary non-privileged port
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)
# conn, addr = s.accept()
# print 'Connected by', addr
# while 1:
#     data = conn.recv(1024)
#     if not data: 
#         break
#     print str(data)
#     sleep(.001)
#     #conn.sendall(data)
# conn.close()


import asyncore, asynchat, socket

class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(5)
    def handle_accept(self):
        newSocket, address = self.accept()
        print "handle accept", address
        SecondaryServerSocket(newSocket)

class SecondaryServerSocket(asynchat.async_chat):
    def __init__(self, *args):
        asynchat.async_chat.__init__(self, *args)
        self.set_terminator('\0')
        self.data = []
    def collect_incoming_data(self, data):
        self.data.append(data)
    def found_terminator(self):
        self.push(''.join(self.data))
        print str(self.data)
        self.data = []
    def handle_close(self):
        print "handle close ", self.getpeername()
        self.close()

MainServerSocket(8888)
while 1:
    asyncore.loop()
