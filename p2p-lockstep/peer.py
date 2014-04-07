from random import randint
from time import sleep

from network import Handler, poll, Listener


listening_port = randint(20000, 30000)
myname = ''  # will be my_ip:listening_port

peer_handlers = {}  # map peer name ('remote ip:listening port') to handler
peer_dir_available = False  # when True, I can init connections to other peers. 

class PeerHandler(Handler):
    
    def on_msg(self, data):
        if 'p2pjoin' in data:
            peer_handlers[data['p2pjoin']] = self
            print '%s: connection from %s' % (myname, data['p2pjoin'])
          

class DirectoryClient(Handler):  # connect to the directory server
    
    def on_msg(self, data):  
        if 'welcome' in data:
            # receive directory: list of [IP, port]
            # then connect to all those peers 
            global myname
            myname = data['welcome']['your_name']
            for name in data['welcome']['names']:
                ip, port = str(name).split(':')
                ph = PeerHandler(ip, int(port))
                peer_handlers[name] = ph
                ph.do_send({'p2pjoin': myname})
            global peer_dir_available 
            peer_dir_available = True
    
# Establish connection with the directory server.
dir_client = DirectoryClient('localhost', 8888)  # async connect
while not dir_client.connected:
    poll()
    sleep(0.01)
print '%d connected to directory' % listening_port

# Send the P2P port I will be listening to. (The dir server has my IP already)
# Receive in response the list of (IP, port) of peers in the network.
dir_client.do_send({'my_port': listening_port})
while not peer_dir_available:
    poll()
    sleep(0.01)
print '%s knows about peers: %s' % (myname, str(peer_handlers.keys()))

# Listen to incoming P2P connections from future peers.
class PeerListener(Listener):
    handlerClass = PeerHandler
listener = PeerListener(listening_port)


while 1:
    sleep(0.1)  # seconds
    poll()  # 1 P2P listener, 1 directory client, and N-1 P2P handlers 
