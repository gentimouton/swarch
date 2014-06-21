"""
Node connecting to the broker like a normal player, 
except it stores an up-to-date game state by subscribing to all in-game events,
and it runs the whole game with its own tick.
"""
from __future__ import division  # So to make division be float instead of int

from network import poll_for, Handler
from random import randint
import time

##################### game logic #############
TICK_DURATION = 0.05  # seconds
# game state
borders = [[0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2]]
pellets = [[randint(10, 390), randint(10, 290), 5, 5] for _ in range(4)]
players = {}  # map a player name to a player object 

    
# map inputs received from clients to directions
input_dir = {'up': [0, -1], 'down': [0, 1],
             'left': [-1, 0], 'right': [1, 0]}

class Player:

    def __init__(self, name):
        self.name = name
        self.revive()

    def revive(self):
        self.box = [randint(10, 380), randint(10, 280), 10, 10]
        self.dir = input_dir['down']  # original direction: downwards
        self.speed = 2
    
    def change_dir(self, inputt):
        self.dir = input_dir[inputt]
        
    def move(self):
        self.box[0] += self.dir[0] * self.speed
        self.box[1] += self.dir[1] * self.speed
        
    def grow_and_slow(self, qty=2):
        self.box[2] += qty
        self.box[3] += qty
        self.speed -= self.speed / 6
    
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

event_queue = []  # list of events 
# events can be 

class GameManager(Handler):
    
    def on_open(self):
        self.do_send(('_sub', 'join'))
        self.do_send(('_sub', 'change_dir'))
        
    def on_msg(self, data):
        mtype, mdata = data
        event_queue.append((mtype, mdata))
        
gm = GameManager('localhost', 8888)  # connect asynchronously, as a node


######################### loop #######################

def apply_events():
    # apply events onto game state
    global event_queue
    for mtype, mdata in event_queue:
        if mtype == 'join' and mdata not in players: 
            # players should provide a unique name to identify themselves
            players[mdata] = Player(mdata) 
        elif mtype == 'change_dir':
            pname, dir = mdata
            players[pname].change_dir(dir)
    event_queue = []
    
def update_simulation():
    [player.update() for player in players.values()]
    
def publish_state():
    # Send the whole game state
    serialized_players = {p.name: p.box for p in players.values()}
    state = {'borders': borders,
             'pellets': pellets,
             'players': serialized_players}
    gm.do_send(('state', state))

while 1:
    loop_start = time.time()
    apply_events()
    update_simulation()
    publish_state()
    poll_for(TICK_DURATION - (time.time() - loop_start))  # poll until tick is over
