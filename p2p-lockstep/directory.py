""" 
Directory: Give the list of connected peers when asked for it.
Keep an up-to-date directory by receiving periodic heartbeats from the peers.
""" 

from time import sleep

from network import Listener, Handler, poll


peers = {}  # map peer name ('ip:port') to handler 

class MyHandler(Handler):
    
    def on_open(self):
        pass
        
    def on_close(self):
        del peers[self.name]
        
    def on_msg(self, data):
        if 'my_port' in data:
            # name is 'remote IP:P2P port'
            self.name = ':'.join([self.addr[0], str(data['my_port'])])  
            self.do_send({'welcome': {'names': peers.keys(),
                                      'your_name': self.name}})
            peers[self.name] = self
            print 'SRV: joined %s' % (self.name)
        

class Server(Listener):
    handlerClass = MyHandler

server = Server(8888)

while 1:
    poll()
    sleep(.05)
