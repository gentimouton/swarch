"""
Streaming server:
- process inputs received from clients
- update game state
- render game state into a screenshot
- send the screenshot to the clients 
"""
from __future__ import division  # division returns float instead of int

import base64
from network import Listener, Handler, poll
from random import randint
import time
import zlib

import pygame


pygame.init()

WIDTH, HEIGHT = 400, 300  # pixels
TICK_DURATION = 0.02  # seconds

##################### game logic #############
# game state
borders = [[0, 0, 2, HEIGHT], [0, 0, WIDTH, 2],
           [WIDTH - 2, 0, 2, HEIGHT], [0, HEIGHT - 2, WIDTH, 2]]
pellets = [[randint(10, WIDTH - 10),
            randint(10, HEIGHT - 10), 5, 5] for _ in range(4)]
players = {}  # map a client handler to a player object 

player_id = 0
def generate_name():
    global player_id
    player_id += 1
    return str(player_id)
    
# map inputs received from clients to directions
input_dir = {'up': [0, -1], 'down': [0, 1],
             'left': [-1, 0], 'right': [1, 0]}

class Player:
    
    def __init__(self):
        self.name = generate_name()
        self.revive()

    def revive(self):
        self.box = [randint(10, WIDTH - 10), randint(10, HEIGHT - 10), 10, 10]
        self.dir = input_dir['down']  # original direction: downwards
        self.speed = 2
    
    def change_dir(self, input):
        self.dir = input_dir[input]
        
    def move(self):
        self.box[0] += self.dir[0] * self.speed
        self.box[1] += self.dir[1] * self.speed
        
    def grow_and_slow(self, qty=2):
        self.box[2] += qty
        self.box[3] += qty
        self.speed -= self.speed / 6

def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1
     
################### network ##############

event_queue = []  # list of ('event', handler) 
# 'event' can be 'quit', 'join', 'up', 'down', 'left', 'right'

class MyHandler(Handler):
    """ Send screenshots in base 64 + gzip, 
    receive player inputs in JSON.
    """
    def encode(self, msg):
        return base64.b64encode(zlib.compress(msg))
            
    def on_open(self):
        event_queue.append(('join', self))
        
    def on_close(self):
        event_queue.append(('quit', self))
        
    def on_msg(self, data):
        event_queue.append((data['input'], self))
    

Listener(8888, MyHandler)

######################### loop #######################

def apply_client_events():
    # apply events onto game state
    global event_queue   
    for event, handler in event_queue: 
        if event == 'quit':
            del players[handler]
        elif event == 'join':
            players[handler] = Player()
        else:  # movement input
            players[handler].change_dir(event)
    event_queue = []
    
    
def update_avatars():
    # move everyone and detect collisions
    for player in players.values():  
        player.move()
        for border in borders:  # collision with borders
            if collide_boxes(player.box, border):
                player.revive()
        for p in players.values():  # collision with other players
             # only the player with lowest id of the pair detects the collision
            if player.name < p.name and collide_boxes(player.box, p.box):
                playerw, pw = player.box[2], p.box[2]  # widths
                if playerw > pw:
                    player.grow_and_slow(pw)
                    p.revive()
                elif playerw < pw:
                    p.grow_and_slow(playerw)
                    player.revive()
                else:  # they have same width: kill both 
                    p.revive()
                    player.revive()
        for index, pellet in enumerate(pellets):  # collision with pellets
            if collide_boxes(player.box, pellet):
                player.grow_and_slow()
                pellets[index] = [randint(10, WIDTH - 10),
                                  randint(10, HEIGHT - 10), 5, 5]

    
def render(handler):
    # render game state into a surface. This rendering varies for each player.
    screen = pygame.Surface((WIDTH, HEIGHT))
    screen.fill((0, 0, 64))  # dark blue
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
    [pygame.draw.rect(screen, (255, 0, 0), p.box) for h, p in players.items() if h != handler]
    pygame.draw.rect(screen, (0, 191, 255), players[handler].box)
    return screen

   
while 1:
    loop_start = time.time()
    
    # enqueue the player events received by the client handlers
    apply_client_events()
    update_avatars()
    
    # render and send screenshot
    for h in players.keys():
        surface = render(h) 
        msg = pygame.image.tostring(surface, 'RGB') 
        h.do_send(msg)

    # poll until the tick is over
    while time.time() - loop_start < TICK_DURATION:
        poll(TICK_DURATION - (time.time() - loop_start))

