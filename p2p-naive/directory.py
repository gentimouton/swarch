""" 
Directory: Give the list of connected peers when asked for it.
Keep an up-to-date directory by receiving periodic heartbeats from the peers.
""" 

from network import Listener, Handler, poll


peers = set()

class MyHandler(Handler):
    
    def on_close(self):
        peers.remove(self)
        
    def on_msg(self, data):
        mtype = data['mtype']
        if mtype == 'join_dir':
            self.ip_port = data['ip_port']
            self.do_send({'mtype': 'welcome',
                          'others_ip_port': [p.ip_port for p in peers]})
            peers.add(self)
            

Listener(8888, MyHandler)

while 1:
    poll(timeout=.1)  # seconds
