""" 
Directory: Give the list of connected peers when asked for it.
Keep an up-to-date directory by receiving periodic heartbeats from the peers.
""" 

from time import sleep

from network import Listener, Handler, poll


peers = {}  # map peer 'ip:port' to handler 

class MyHandler(Handler):
    
    def on_open(self):
        pass
        
    def on_close(self):
        del peers[self.ip_port]
        
    def on_msg(self, data):
        if 'my_port' in data:
            self.ip_port = ':'.join([self.addr[0], str(data['my_port'])])
            self.do_send({'welcome': {'others_ip_port': peers.keys(),
                                      'your_ip_port': self.ip_port}})
            peers[self.ip_port] = self
            print 'SRV: joined %s' % (self.ip_port)
        

server = Listener(8888, MyHandler)

while 1:
    poll(timeout=.1) # seconds
