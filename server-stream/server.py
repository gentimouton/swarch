"""
Streaming server:
- process inputs received from clients
- update game state every tick
- render game state into a buffer
- send the buffer to the clients 
"""
from __future__ import division  # So to make division be float instead of int

from base64 import b64encode
from network import Listener, Handler, poll
from random import randint
from time import sleep
import time

import pygame
from pygame.draw import rect as draw_rect


pygame.init()


##################### game logic #############
# game state
borders = [[0, 0, 2, 60], [0, 0, 80, 2], [78, 0, 2, 30], [0, 58, 80, 2]]
pellets = [[randint(10, 70), randint(10, 50), 5, 5] for _ in range(4)]
players = {}  # map a client handler to a player object 
screen = pygame.Surface((80, 60))

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
        self.box = [randint(10, 70), randint(10, 50), 10, 10]
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
                pellets[index] = [randint(10, 70), randint(10, 50), 5, 5]

    
def render():
    # render game state into a surfarray
    screen.fill((0, 0, 64))  # dark blue
    [draw_rect(screen, (0, 191, 255), b) for b in borders]  # deep sky blue 
    [draw_rect(screen, (255, 192, 203), p) for p in pellets]  # shrimp
    for name, p in players.items():
        draw_rect(screen, (255, 0, 0), p.box)  # red
    pg_array = pygame.surfarray.array3d(screen)  # serialize
    return pg_array

   
while 1:   
    # enqueue the player events received by the client handlers
    before = time.time()
    poll()
    apply_client_events()
    update_avatars()
    pg_array = render()
    msg = {'dtype': str(pg_array.dtype),
           'b64array': b64encode(pg_array),
           'shape': pg_array.shape}
    [handler.do_send(msg) for handler in players.keys()]
    print 'server frame: %3.0f ms' % ((time.time() - before) * 1000)
    sleep(0.1)  # seconds
