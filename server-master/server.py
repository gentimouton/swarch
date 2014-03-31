"""
Server master:
The server is almighty. 
The server regularly sends the WHOLE game state to the clients.
The clients do not interpolate player commands. 
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
        
    def on_msg(self, data):
        msgtype = data['msg_type']
        
              
class Server(Listener):
    handlerClass = MyHandler

server = Server(8888)

# loop
while 1:
    poll()
    sleep(.05)  # seconds
