"""
Message broker.
Clients publish movement events.
Broker delivers an event to a client only if the event happened near the client.
"""
from __future__ import division # So to make division be float instead of int

from network import poll_for, Listener, Handler
from random import randint
import time
import uuid


##################### game logic #############
TICK_DURATION = 0.05  # seconds
# game state
borders = [[0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2]]
pellets = [[randint(10, 390), randint(10, 290), 5, 5] for _ in range(4)]
players = {}  # map a client handler to a player object 


# map inputs received from clients to directions
input_dir = {'up': [0, -1],
             'down': [0, 1],
             'left': [-1, 0],
             'right': [1, 0]
             }

class Player:
    
    def __init__(self):
        self.name = str(uuid.uuid4())
        self.revive()

    def revive(self):
        x, y, w, h = randint(10, 380), randint(10, 280), 10, 10
        self.box = [x, y, w, h]
        self.frustum = [x - 50, y - 50, 2 * 50 + w, 2 * 50 + h]
        self.dir = input_dir['down']  # original direction: downwards
        self.speed = 2 # pixels per frame
    
    def change_dir(self, inputt):
        self.dir = input_dir[inputt]
        
    def move(self):
        dx = self.dir[0] * self.speed
        dy = self.dir[1] * self.speed
        self.box[0] += dx
        self.box[1] += dy
        self.frustum[0] += dx
        self.frustum[1] += dy
        
    def grow_and_slow(self, qty=2):
        self.box[2] += qty
        self.box[3] += qty
        self.speed -= self.speed / 10 # float if from __future__ import division
        self.frustum[2] += qty
        self.frustum[3] += qty
        
    def collide_borders(self):
        [self.revive() for border in borders if collide_boxes(self.box, border)]
        
    def collide_other_players(self):
        for p in players.values(): 
            # only the player with lowest id of the pair detects the collision
            if self.name < p.name and collide_boxes(self.box, p.box):
                playerw, pw = self.box[2], p.box[2]  # widths
                if playerw > pw:
                    self.grow_and_slow(pw)
                    p.revive()
                elif playerw < pw:
                    p.grow_and_slow(playerw)
                    self.revive()
                else:  # they have same width: kill both 
                    p.revive()
                    self.revive()
    
    def collide_pellets(self):
        for index, pellet in enumerate(pellets):
            if collide_boxes(self.box, pellet):
                self.grow_and_slow()
                pellets[index] = [randint(10, 390), randint(10, 290), 5, 5]
    
    def can_see(self, box):
        return collide_boxes(self.frustum, box)
            
    def update(self):
        self.move()
        self.collide_borders()
        self.collide_other_players()
        self.collide_pellets()
        
        
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

def apply_events():
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
    
def update_simulation():
    [player.update() for player in players.values()]
        
def broadcast_state():
    for h, p in players.items():
        blist = [b for b in borders if p.can_see(b)]
        plist = [p2 for p2 in pellets if p.can_see(p2)]
        pdic = {p2.name: p2.box for p2 in players.values() if p.can_see(p2.box)}
        msg = {'borders': blist,
               'pellets': plist,
               'myname': p.name,
               'players': pdic,
               'frustum': p.frustum}
        h.do_send(msg)
           
                
while 1:
    loop_start = time.time()
    apply_events()
    update_simulation()
    broadcast_state()
    poll_for(TICK_DURATION - (time.time() - loop_start))  # poll until tick is over
