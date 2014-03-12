from time import sleep
from network import Listener, Handler, poll
from random import randint

# gameplay 

pellets = []
for _ in range(4):  # 4 pellets in the game
    pellets.append([randint(0, 390), randint(0, 290), 5, 5])

players = {}  # map id to rectangle
player_id = 0
def add_player():
    player_id += 1
    players[player_id] = [randint(0, 390), randint(0, 290), 10, 10]
    return player_id 

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
            broadcast({'msg_type': 'move',
                       'name': self.myname,
                       'state': data['state']})
            
        elif msgtype == 'eat':  # replace pellet, grow player, and forward new game state
            p_index = data['pellet_index']
            pellets[p_index] = [randint(0, 390), randint(0, 290), 5, 5]
            w, h = players[self.myname][2] * 1.2, players[self.myname][3] * 1.2
            players[self.myname][2] = w
            players[self.myname][3] = h
            
            broadcast({'msg_type': 'eat',
                       'name': self.myname,
                       'pellet_index': p_index,
                       'new_pellet': pellets[p_index],
                       'size': [w, h]})
        
              
class Server(Listener):
    handlerClass = MyHandler

server = Server(8888)


# loop
while 1:
    poll()
    sleep(.05)  # 50ms, 20 frames per second
