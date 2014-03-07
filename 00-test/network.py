import asynchat
import asyncore
import socket
from time import sleep

from rencode import loads, dumps


_terminator = '\0'

def _make_TCP_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # don't use Nagle's algorithm
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    return sock



class BaseHandler(asynchat.async_chat):
    
    def __init__(self, sock):
        self._rcv_buffer = ''
        self.set_terminator(_terminator)
        asynchat.async_chat.__init__(self, sock)

    def collect_incoming_data(self, data):
        self._rcv_buffer += data

    def found_terminator(self):
        data = loads(self._rcv_buffer)
        self._rcv_buffer = ''
        self._nw.on_msg(self, data)
        
    def handle_close(self):
        asyncore.dispatcher.close()  # close the socket
        self._nw.on_close(self)
        
    def handler_error(self):
        self._nw.on_error(self)
        
    def do_send(self, data):
        # asyncore.dispatcher.send() already exists, therefore do_send()
        msg_to_send = dumps(data) + _terminator
        self.push(msg_to_send)
    
    def do_close(self, handler):
        handler.handle_close() # will call on_close
         

class Handler(BaseHandler):
    """ A Handler that can connect to a listening socket.
    """

    def __init__(self, host, port):
        sock = _make_TCP_socket()
        BaseHandler.__init__(self, sock)
        self.connect((host, port)) # asynchronous/non-blocking socket opening 
        
    def handle_connect(self):
        print 'client connected'
        self.on_open()

    def connect(self, host, port, blocking=True):
        if blocking: # keep polling until the socket returns
            while not self.connected: 
                poll()
        # return handler # TODO: should I return it?
    
        
        
class Listener(asyncore.dispatcher):
    """ Create a handler for each incoming connection.
    """
    
    def __init__(self, port):
        sock = _make_TCP_socket()
        asyncore.dispatcher.__init__(self, sock)
        self.bind(('', port))
        # Windows won't allow more than 5 connections at once. 
        # http://docs.python.org/2/library/socket.html#socket.socket.listen
        self.listen(5)

    def handle_accept(self):
        # Called someone tries to connect to our socket.
        sock, addr = self.accept()
        BaseHandler(sock)
        #self._nw.on_open(h) # TODO: move this to the Handler
    
    def stop(self):
        self.handle_close() # asyncore method, closes listening socket
        

   
    



def poll(self):
    asyncore.loop(count=1) # poll sockets once, then return
        
        
    
    # override these callbacks
    def on_open(self, handler):
        print '%s opened' % str(handler.addr)
    
    def on_msg(self, handler, data):
        print '%s received %s' % (str(handler.addr), str(data))
    
    def on_close(self, handler):
        print '%s closed' % str(handler.addr)
    
    def on_error(self, handler):
        print '%s error' % str(handler.addr)
    

