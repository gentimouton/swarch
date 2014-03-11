from time import sleep

from network import Listener, Handler, poll


class MyHandler(Handler):
    
    server = None # replaced by Server.on_accept
    
    def on_open(self):
        self.myname = ''
        self.server.add_handler(self)
        
    def on_close(self):
        self.server.remove_handler(self)
        self.server.broadcast({'msgtype': 'leave', 'name': self.myname})
        
    def on_msg(self, data):
        msgtype = data['msgtype']
        name = data['name']
        if msgtype == 'join':  # the player joined: forward his/her name
            self.myname = name
            self.server.broadcast({'msgtype': 'join', 'name': name})
        elif msgtype == 'move':
            top, left = data['top'], data['left']
            self.server.broadcast({'msgtype': 'move', 'name': name,
                                   'top': top, 'left': left})
            
            
class Server(Listener):
    
    handlerClass = MyHandler
    handlers = set()
    
    def on_accept(self, handler):
        handler.server = self
        self.handlers.add(handler)
        
    def broadcast(self, msg):
        copies = self.handlers.copy()  # avoid "Set changed size during iteration"
        [h.do_send(msg) for h in copies]
    
    def add_handler(self, h):
        self.handlers.add(h)
        
    def remove_handler(self, h):
        self.handlers.remove(h)
    

server = Server(8888)
while 1:
    poll()
    sleep(.1)