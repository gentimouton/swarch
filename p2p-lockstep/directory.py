""" 
Directory: Give the list of connected peers when asked for it.
Keep an up-to-date directory by receiving periodic heartbeats from the peers.
""" 

from network import Listener, Handler, poll
from time import sleep


peers = {}  # map each handler to the p2p listening port on the remote peer

class MyHandler(Handler):
    
    def on_open(self):
        pass
        
    def on_close(self):
        del peers[self]
        
    def on_msg(self, data):
        if 'join' in data:
            peer_list = [[h.addr[0], port] for (h, port) in peers.items()] 
            self.do_send({'directory': peer_list})  # (IP, port) list
            peers[self] = data['join']
            print '%s joined, listening on port %d' % (str(self.addr), data['join'])
        

class Server(Listener):
    handlerClass = MyHandler

server = Server(8888)

while 1:
    poll()
    sleep(.05)
