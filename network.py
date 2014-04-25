"""
Simple JSON wrapper on top of asyncore TCP sockets. 
Provides on_open, on_close, on_msg, do_send, and do_close callbacks.

Public domain

With inspiration from:
http://pymotw.com/2/asynchat/
http://code.google.com/p/podsixnet/
http://docstore.mik.ua/orelly/other/python/0596001886_pythonian-chp-19-sect-3.html


#################
# Echo server:
#################
from network import Listener, Handler, poll

class MyHandler(Handler):
    def on_msg(self, data):
        self.do_send(data)

server = Listener(8888, MyHandler)
while 1:
    poll()


#################
# One-message client:
#################
from network import Handler, poll

done = False

class Client(Handler):
    def on_open(self):
        self.do_send({'a': [1,2], 5: 'hi'})
        global done
        done = True

client = Client('localhost', 8888)
while not done:
    poll()
client.do_close()

"""

import asynchat
import asyncore
import json
import os
import socket


class Handler(asynchat.async_chat):
    
    def __init__(self, host, port, sock=None):
        if sock:  # passive side: Handler automatically created by a Listener
            asynchat.async_chat.__init__(self, sock)
        else:  # active side: Handler created manually
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
            asynchat.async_chat.__init__(self, sock)
            self.connect((host, port))  # asynchronous and non-blocking
        self.set_terminator('\0')
        self._buffer = []
        
    def collect_incoming_data(self, data):
        self._buffer.append(data)

    def found_terminator(self):
        msg = json.loads(''.join(self._buffer))
        self._buffer = []
        self.on_msg(msg)
    
    def handle_close(self):
        self.close()
        self.on_close()

    def handle_connect(self):  # called on the active side
        self.on_open()
        
    # API you can use
    def do_send(self, msg):
        self.push(json.dumps(msg) + '\0')
        
    def do_close(self):
        self.handle_close()  # will call self.on_close
    
    # callbacks you should override
    def on_open(self):
        pass
        
    def on_close(self):
        pass
        
    def on_msg(self, data):
        pass
    
    
class Listener(asyncore.dispatcher):
    
    def __init__(self, port, handler_class):
        asyncore.dispatcher.__init__(self)
        self.handler_class = handler_class
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        self.bind(('', port))
        self.listen(5)  # max 5 incoming connections at once (Windows' limit)

    def handle_accept(self):  # called on the passive side
        accept_result = self.accept()
        if accept_result:  # None if connection blocked or aborted
            sock, (host, port) = accept_result
            h = self.handler_class(host, port, sock)
            self.on_accept(h)
            h.on_open()
    
    # API you can use
    def stop(self):
        self.close()

    # callbacks you override
    def on_accept(self, h):
        pass
    
    
def poll(timeout=0):
    asyncore.loop(timeout=timeout, count=1)  # return right away


def get_my_ip():
    """ Get my network interface's IP, not localhost's IP.
    From http://stackoverflow.com/a/1947766/856897
    """
    ip = socket.gethostbyname(socket.gethostname())
    # Some versions of Ubuntu may return 127.0.0.1
    if os.name != "nt" and ip.startswith("127."):
        import fcntl  # not available on Windows
        import struct
        interfaces = ["eth0", "eth1", "eth2", "wlan0",
                      "wlan1", "wifi0", "ath0", "ath1", "ppp0"]
        for ifname in interfaces:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                                  0x8915,  # SIOCGIFADDR
                                                  struct.pack('256s', ifname[:15])
                                                  )[20:24])
                break;
            except IOError:
                pass
    return ip


                
if __name__ == '__main__':
    print get_my_ip()
