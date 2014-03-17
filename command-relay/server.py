"""
Known bug:
- If a big box goes upwards slowly, and a small box below it goes upwards fast,
then the collision is only detected on the small client, not on the big client.
 
"""
from random import randint
from time import sleep
import time

from network import Listener, Handler, poll


# gameplay 
pellets = []
for _ in range(4):  # 4 pellets in the game
    pellets.append([randint(10, 390), randint(10, 290), 5, 5])
    
players = {}  # map name to rectangle
player_id = 0
def add_player():
    global player_id
    player_id += 1
    players[str(player_id)] = [randint(0, 280), randint(0, 380), 10, 10]
    return str(player_id) 

# network 

handlers = set()
def broadcast(msg):
    copies = handlers.copy()  # avoid "Set changed size during iteration" error
    [h.do_send(msg) for h in copies]

class MyHandler(Handler):
        
    def on_open(self):
        self.myname = add_player()  # create a new player
        handlers.add(self)
        self.do_send({'msg_type': 'welcome',
                      'name': self.myname,
                      'players': players,
                      'pellets': pellets})  # send him the whole game state
        broadcast({'msg_type': 'join',
                   'name': self.myname,
                   'state': players[self.myname]})  # tell everyone about him
        
    def on_close(self):
        del players[self.myname]
        handlers.remove(self)
        broadcast({'msg_type': 'leave', 'name': self.myname})
        
    def on_msg(self, data):
        msgtype = data['msg_type']
        
        if msgtype == 'move':  # forward the move to everyone
            players[self.myname] = data['state']
            broadcast({'msg_type': 'move',
                       'name': self.myname,
                       'state': data['state']})
            
        elif msgtype == 'eat_pellet':  # replace pellet and grow player
            p_index = data['pellet_index']
            pellets[p_index] = [randint(10, 390), randint(0, 290), 5, 5]
            w, h = players[self.myname][2] + 2, players[self.myname][3] * + 2
            players[self.myname][2] = w
            players[self.myname][3] = h
            broadcast({'msg_type': 'eat_pellet',
                       'name': self.myname,
                       'pellet_index': p_index,
                       'new_pellet': pellets[p_index],
                       'size': [w, h]})
    
        elif msgtype == 'eat_player':  # grow the big by the size of the small
            small = players[data['target']]
            players[self.myname][2] += small[2]
            players[self.myname][3] += small[3]
            broadcast({'msg_type': 'grow',
                       'name': self.myname,
                       'size': [players[self.myname][2],
                                players[self.myname][3]]})
            
        elif msgtype == 'die':  # back to normal size and place me randomly
            players[self.myname] = [randint(0, 280), randint(0, 280), 10, 10]
            broadcast({'msg_type': 'die',
                       'name': self.myname,
                       'state': players[self.myname]})
        
              
class Server(Listener):
    handlerClass = MyHandler

server = Server(8888)

# loop
while 1:
    poll()
    sleep(.05)  # seconds
