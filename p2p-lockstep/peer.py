from random import randint
from time import sleep

from network import Handler, poll, Listener


listening_port = randint(20000, 40000)  # random port in 20-40k

peer_dir = {}
peer_dir_available = False  # when True, I can init connections to other peers. 

class PeerHandler(Handler):
    def on_open(self):
        print '%d connected with %s' % (listening_port, str(self.addr))
        
    def on_msg(self, data):
        print '%d received %s from peer %s' % (listening_port, str(data), str(self.addr))

class DirectoryClient(Handler):  # connect to the directory server
    
    def on_msg(self, data):  # receive directory: list of [IP, port]
        # then connect to all those peers 
        for (ip, port) in data['directory']:
            peer_dir[str(ip) + ':' + str(port)] = PeerHandler(str(ip), port)
        global peer_dir_available 
        peer_dir_available = True
    
# Establish connection with the directory server.
dir_client = DirectoryClient('localhost', 8888)  # async connect
while not dir_client.connected:
    poll()
    sleep(0.01)
print '%d connected' % listening_port

# Send the P2P port I will be listening to. (The dir server has my IP already)
# Expect in response the list of (IP, port) of peers in the network.
dir_client.do_send({'join': listening_port})
while not peer_dir_available:
    poll()
    sleep(0.01)
print '%d recv %d peers' % (listening_port, len(peer_dir))

# wait for incoming P2P connections from the peers who will join after me
class PeerListener(Listener):
    handlerClass = PeerHandler

listener = PeerListener(listening_port)

while 1:
    sleep(0.1)
    poll()  # poll 1 listener and N client(s)
    