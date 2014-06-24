from network import Handler, poll_for, Listener, get_my_ip, poll
from random import randint, choice
import time

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


TICK_DURATION = 0.02  # seconds
DIRECTORY_HOST = 'localhost'
my_port = randint(20000, 30000)
my_ip_port = get_my_ip() + ':' + str(my_port)

peers = set()  # collection of Peer

borders = [[0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2]]
pellets = []  # shared state: created if I'm first peer, fetched otherwise

mybox = None
def place_my_box():
    global mybox
    mybox = [200, 150, 10, 10]
place_my_box()

mydir = K_DOWN


    
###################### p2p networking ##########################
     
class Peer(Handler):
    """ P2P connection handler. Also store the box of the remote player.    
    """
    
    def __init__(self, host, port, sock=None):
        self.ip_port = None  # set when that player sends a 'join' message
        self.box = None  # updated when that player moves
        Handler.__init__(self, host, port, sock=sock)
        
        
    def on_close(self):
        peers.remove(self)
        
        
    def on_msg(self, data):
        mtype = data['mtype']
        
        if mtype == 'join':  # remote peer joined the game
            peers.add(self)
            self.ip_port = data['ip_port']

        elif mtype == 'pellet_request':  # peer asked for list of pellets
            self.do_send({'mtype': 'pellet_response',
                          'pellets': pellets})
            
        elif mtype == 'pellet_response':  # peer sent list of pellets
            pellets[:] = data['pellets']
            
        elif mtype == 'position':
            self.box = data['box']
            
        elif mtype == 'death':
            self.box = data['newbox']
            
        elif mtype == 'eat_pellet':
            pellets[data['pellet_index']] = data['new_pellet']
            
        elif mtype == 'collide_with':  # peer collided with someone
            if data['ip_port'] == my_ip_port:  # peer collided with me
                place_my_box()  # TODO: send death message too?
            
            
        
#####################################################################   


def fetch_pellets():
    handler = choice(list(peers))
    handler.do_send({'mtype': 'pellet_request'})
    
def create_pellets():
    global pellets
    pellets = [[randint(10, 390), randint(10, 290), 5, 5] for _ in range(4)]
    
##################### directory networking #############################
    
class DirectoryClient(Handler):  # connect to the directory server
    
    def __init__(self, host, port):
        self.directory_received = False
        Handler.__init__(self, host, port)
        
    def on_msg(self, data):
        mtype = data['mtype']  
        if mtype == 'welcome':
            self.directory_received = True
            others_ip_port = data['others_ip_port']
            self.connect_to_peers(others_ip_port)
            # create pellets if I'm the only peer, fetch them otherwise
            if others_ip_port:  # other peers have pellets data
                fetch_pellets()
            else:
                create_pellets()
                
    def connect_to_peers(self, ip_ports):
        for ip_port in ip_ports:
            ip, port = str(ip_port).split(':')
            peer = Peer(ip, int(port))
            peers.add(peer)
            peer.ip_port = ip_port
            peer.do_send({'mtype': 'join',
                          'ip_port': my_ip_port})
            print 'Connected to %s.' % ip_port  

# Establish connection with the directory server.
dir_client = DirectoryClient(DIRECTORY_HOST, 8888)  # async connect
while not dir_client.connected:
    poll(timeout=.1)  # seconds
print 'Connected to the directory server.'

# Send the IP and port I will be listening to.
# Receive in response the list of (IP, port) of peers in the network.
dir_client.do_send({'mtype': 'join_dir',
                    'ip_port': my_ip_port})
while not dir_client.directory_received:
    poll(timeout=.1)  # seconds
print 'Retrieved a directory of %d peers.' % len(peers)

# Listen to incoming P2P connections from future peers.
p2p_listener = Listener(my_port, Peer)


pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()


def broadcast(msg):
    for handler in peers:
        handler.do_send(msg)
        
def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1
    
################### inputs ################ 

valid_inputs = {K_UP: (0, -1), K_DOWN: (0, 1), K_LEFT: (-1, 0), K_RIGHT: (1, 0)}

def process_inputs():
    # send valid inputs to the server
    for event in pygame.event.get():  
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                exit()
            elif key in valid_inputs and mybox:
                global mydir
                mydir = key

################ gameplay #################

def update_me():
    dx, dy = valid_inputs[mydir]
    mybox[0] += dx
    mybox[1] += dy
    collide_borders()
    collide_pellets()
    collide_players()
    
def collide_borders():
    for b in borders:
        if collide_boxes(mybox, b):
            place_my_box()
            broadcast({'mtype': 'death',
                       'newbox': mybox})
            break  # only send 'die' once

def collide_pellets():
    pellets_copy = pellets[:]
    for p_idx, p in enumerate(pellets_copy):
        if collide_boxes(mybox, p):
            mybox[2] *= 1.2
            mybox[3] *= 1.2
            new_pellet = [randint(10, 390), randint(10, 290), 5, 5]
            pellets[p_idx] = new_pellet
            broadcast({'mtype': 'eat_pellet',
                       'pellet_index': p_idx,
                       'new_pellet': new_pellet})

def collide_players():
    for p in peers:
        b = p.box
        if b and collide_boxes(mybox, b):
            if mybox[2] > b[2]:  # I am bigger
                mybox[2] *= 1.2
                mybox[3] *= 1.2
                broadcast({'mtype': 'collide_with',
                           'ip_port': p.ip_port})
            elif mybox[2] == b[2] and my_ip_port > p.ip_port:
                place_my_box()
                broadcast({'mtype': 'collide_with',
                           'ip_port': p.ip_port})

############### graphics ###############

def draw_everything():
    screen.fill((0, 0, 64))  # dark blue
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  
    [pygame.draw.rect(screen, (255, 0, 0), p.box) for p in peers if p.box]
    pygame.draw.rect(screen, (0, 191, 255), mybox) 
    pygame.display.update()
    
################### loop ################ 

while 1:
    loop_start = time.time()
    process_inputs()
    update_me()
    broadcast({'mtype': 'position', 'box': mybox})
    draw_everything()
    poll_for(TICK_DURATION - (time.time() - loop_start))  # poll until tick is over

    
