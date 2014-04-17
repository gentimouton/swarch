"""
Server master:
The server is almighty. 
Every frame, it receives player inputs from clients,
executes these inputs to update the game state,
and sends the whole game state to all the clients for display. 
"""
from __future__ import division # So to make division be float instead of int
from network import Listener, Handler, poll
from random import randint
from time import sleep


##################### game logic #############
# game state
borders = [[0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2]]
pellets = [[randint(10, 390), randint(10, 290), 5, 5] for _ in range(4)]
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
        self.box = [randint(10, 380), randint(10, 280), 10, 10]
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
        self.speed -= self.speed/6

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
    

server = Listener(8888, MyHandler)

######################### loop #######################

while 1:
    
    # enqueue the player events received by the client handlers
    poll()
    
    # apply events onto game state
    for event, handler in event_queue: 
        if event == 'quit':
            del players[handler]
        elif event == 'join':
            players[handler] = Player()
        else:  # movement input
            players[handler].change_dir(event)
    event_queue = []
    
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
                pellets[index] = [randint(10, 390), randint(10, 290), 5, 5]
        
    # Send to all players 1) the whole game state, and 2) their own name, 
    # so each player can draw herself differently from the other players.
    serialized_players = {p.name: p.box for p in players.values()}
    for handler, player in players.items():
        msg = {'borders': borders,
               'pellets': pellets,
               'myname': player.name,
               'players': serialized_players}
        handler.do_send(msg)
        
    sleep(1. / 20)  # seconds
