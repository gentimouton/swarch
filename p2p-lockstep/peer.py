from network import Handler, poll
from time import sleep
from random import randint

listening_port = randint(20000, 40000)  # random port in 20-40k

peer_dir = set()
peer_dir_available = False  # when True, I can init connections to other peers. 


class DirectoryClient(Handler):  # connect to the directory server
    
    def on_msg(self, data):  # receive directory: list of [IP, port]
        for (ip, port) in data['directory']:
            peer_dir.update([str(ip) + ':' + str(port)])
        
        global peer_dir_available 
        peer_dir_available = True
        
        
# when the connection is established, send my peer-to-peer listening (IP, port) 
# and fetch the directory of peers already connected 
dir_client = DirectoryClient('localhost', 8888)  # async connect
while not dir_client.connected:
    poll()
    sleep(0.01)
print '%d connected' % listening_port

dir_client.do_send({'join': listening_port})
while not peer_dir_available:
    poll()
    sleep(0.01)
print '%d recv %d peers' % (listening_port, len(peer_dir))

# connect to the peers who are already online
for p in peer_dir:
    print '%d should connect to %s' % (listening_port, p)

while 1:
    sleep(0.1)
    poll()
    

    
