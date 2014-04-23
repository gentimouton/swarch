from random import randint, seed, choice
from time import sleep

from network import Handler, poll, Listener
import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT


listening_port = randint(20000, 30000)
#seed(0)

my_ip_port = ''  # will be my_ip:listening_port

peers = None  # map peer handler to Player. None when not received yet. 

borders = [[0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2]]
pellets = []  # created if I'm first peer, fetched otherwise

        
#####################################################################
     
class PeerHandler(Handler):
        
    def on_close(self):
        del peers[self]
        
    def on_msg(self, data):
        global pellets
        if 'join' in data:
            ip_port = data['join']
            peers[self] = {'ip_port': ip_port, 'box': None}
            print '%s: connection from %s' % (my_ip_port, ip_port)
        elif 'get_pellets' in data:
            self.do_send({'give_pellets': pellets})
            print '%s: gave pellets to %s' % (my_ip_port, peers[self]['ip_port'])
        elif 'give_pellets' in data:
            pellets = data['give_pellets']
            print '%s received pellets from %s' % (my_ip_port, peers[self]['ip_port'])
        elif 'move' in data:
            box = data['move']
            peers[self]['box'] = box
            
            
        
            
        
#####################################################################   

class DirectoryClient(Handler):  # connect to the directory server
    
    def on_msg(self, data):  
        if 'welcome' in data:
            # receive peer directory: list of [IP, port]
            # then connect to all those peers
            global peers, my_ip_port
            peers = {}
            my_ip_port = data['welcome']['your_ip_port']
            others_ip_port = data['welcome']['others_ip_port']
            for ip_port in others_ip_port:
                ip, port = str(ip_port).split(':')
                ph = PeerHandler(ip, int(port))
                peers[ph] = {'ip_port': ip_port, 'box': None} # ip:port, box 
                ph.do_send({'join': my_ip_port})
                print '%s connected to %s' % (my_ip_port, ip_port)    
            # create pellets if I'm first peer, fetch them otherwise
            if others_ip_port:
                handler = choice(peers.keys())
                handler.do_send({'get_pellets': ''})
            else:
                global pellets
                pellets = [[randint(10, 390), randint(10, 290), 5, 5] for _ in range(4)]

            
# Establish connection with the directory server.
dir_client = DirectoryClient('localhost', 8888)  # async connect
while not dir_client.connected:
    poll(timeout=.1)  # seconds
    
# Send the P2P port I will be listening to. (The dir server has my IP already)
# Receive in response the list of (IP, port) of peers in the network.
dir_client.do_send({'my_port': listening_port})
while peers is None:
    poll(timeout=.1)  # seconds
print '%s knows about %d peers' % (my_ip_port, len(peers))

# Listen to incoming P2P connections from future peers.
listener = Listener(listening_port, PeerHandler)


pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
mybox = [200, 150, 10, 10]
dx, dy = 0, 1  # start direction: down

while 1:
    clock.tick(10)
    poll()  # network
    
    for event in pygame.event.get():  # inputs
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                exit()
            elif key == K_UP:
                dx, dy = 0, -1
            elif key == K_DOWN:
                dx, dy = 0, 1
            elif key == K_LEFT:
                dx, dy = -1, 0
            elif key == K_RIGHT:
                dx, dy = 1, 0
    
    mybox[0] += dx
    mybox[1] += dy
    for handler in peers.keys():
        handler.do_send({'move': mybox})
    screen.fill((0, 0, 64))  # dark blue
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  
    [pygame.draw.rect(screen, (255, 0, 0), p['box']) for p in peers.values() if p['box']]
    pygame.draw.rect(screen, (0, 191, 255), mybox) 
    pygame.display.update()
    
