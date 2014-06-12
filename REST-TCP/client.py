from collections import deque
from network import Handler, poll, poll_for
import time

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

############ local game model ############
class Game:
    def __init__(self):
        self.myname = None
        self.borders = []
        self.pellets = []
        self.players = {}
    def set_myname(self, s):
        self.myname = s
    def set_borders(self, box_list):
        self.borders = box_list
    def set_pellets(self, box_list):
        self.pellets = box_list
    def set_players(self, d):
        self.players = d
game = Game()

########### network #################
class Client(Handler):
    
    _request_queue = deque()  # queue of resources to request
    _pending_rsrc_req = None  # URL of the pending resource request
    
    def on_msg(self, data):
        self._pending_rsrc_req = None
        request = self._request_queue.popleft()
        method, resource, req_args, callback = request
        mtype, repr = data['type'], data['representation']
        callback(mtype, repr)
        self._send_next_request()
    
    def _callback_game(self, mtype, repr):
        if mtype == 'app/game+json':
            name = self._obtain(repr['name'], self._callback_name)
            if name:
                game.set_myname(name)
            borders = self._obtain(repr['borders'], self._callback_borders)
            if borders:
                game.set_borders(borders)
            pellets = self._obtain(repr['pellets'], self._callback_pellets)
            if pellets:
                game.set_pellets(pellets)
            players = self._obtain(repr['players'], self._callback_players)
            if players:
                game.set_players(players)
            
    def _callback_name(self, mtype, repr):
        if mtype == 'text/plain':
            game.set_myname(repr)
            
    def _callback_borders(self, mtype, repr):
        if mtype == 'app/boxlist+json':
            borders = [box for box in repr]
            game.set_borders(borders)

    def _callback_pellets(self, mtype, repr):
        if mtype == 'app/boxlist+json':
            pellets = [box for box in repr]
            game.set_pellets(pellets)

    def _callback_players(self, mtype, repr):
        if mtype == 'app/boxlist+json':
            # use enumerate to assign random player names to boxes
            players = dict(enumerate(repr)) # {1: [1,2,3,4], 2: [5,6,7,8]}
            game.set_players(players)
        elif mtype == 'app/boxdict+json':
            # box names are provided
            players = repr            

    def _obtain(self, subdata, callback):
        if 'data' in subdata:
            return subdata['data']
        elif 'link' in subdata:
            self.enqueue_request('GET', subdata['link'], {}, callback)
            return None
    
    def _send_next_request(self):
        if self._pending_rsrc_req is None and self._request_queue:
            method, resource, req_args, cb = self._request_queue[0]
            msg = {'method': method,
                   'resource': resource,
                   'args': req_args
                   }
            self._pending_rsrc_req = resource
            client.do_send(msg)
    
    def enqueue_request(self, method, resource, req_args, callback):
        request = (method, resource, req_args, callback)
        self._request_queue.append(request)
        self._send_next_request()
        
    def fetch_game_state(self):
        if game.myname:
            args = {'name': game.myname} # TODO: bad: out-of-band info
            # how do I know that /game/1 accepts a name argument?
            # need a hypermedia form instead
        else:
            args = {}
        self.enqueue_request('GET', '/game/1', args, self._callback_game)
        while len(self._request_queue) > 0 or self._pending_rsrc_req is not None:
            poll(timeout=0.1)
        
        
client = Client('localhost', 8888)  # connect asynchronously
while not client.connected: # poll until connected
    poll(timeout=0.1)

############## inputs ############
valid_inputs = {K_UP: 'up', K_DOWN: 'down', K_LEFT: 'left', K_RIGHT: 'right'}
def process_inputs():
    # send valid inputs to the server
    for event in pygame.event.get():  
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                exit()
            elif key in valid_inputs:
                msg = {'input': valid_inputs[key]}
                print 'TODO: client should send msg'


############## graphics ############
pygame.display.init()
screen = pygame.display.set_mode((400, 300))

def draw_everything():
    screen.fill((0, 0, 64))  # dark blue
    [pygame.draw.rect(screen, (0, 191, 255), b) for b in game.borders]  # deep sky blue
    [pygame.draw.rect(screen, (255, 192, 203), p) for p in game.pellets]  # shrimp
    for name, box in game.players.items():
        if name != game.myname:
            pygame.draw.rect(screen, (255, 0, 0), box)  # red
    if game.myname and game.myname in game.players:
        pygame.draw.rect(screen, (0, 191, 255), game.players[game.myname])  # deep sky blue
    pygame.display.update()



############# main loop #############
TICK_DURATION = 0.02  # seconds
work_durations = []
while client.connected:
    start = time.time()
    client.fetch_game_state() # blocking
    draw_everything()
    process_inputs()
    work_durations.append(time.time() - start)
    if len(work_durations) >= 50:  # average over X frames
        avg_dur = sum(work_durations) / len(work_durations)
        print 'Average work duration: %.0f ms' % (avg_dur * 1000)
        work_durations = []
    poll_for(TICK_DURATION - (time.time() - start)) # throttling
