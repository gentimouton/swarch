from network import Handler, poll
from collections import deque
import time

class Game:
    def __init__(self):
        self.name = None
        self.borders = []
    def set_name(self, name):
        self.name = name
    def set_borders(self, borders):
        self.borders = borders
game = Game()


class Client(Handler):
    
    _request_queue = deque()  # queue of resources to request
    _pending_rsrc_req = None  # URL of the pending resource request
    
    def in_steady_state(self):
        return (len(self._request_queue) == 0 and self._pending_rsrc_req is None) 
    
    def on_msg(self, data):
        self._pending_rsrc_req = None
        request = self._request_queue.popleft()
        method, resource, req_args, callback = request
        mtype, repr = data['type'], data['representation']
        callback(mtype, repr)
        self.send_next_request()
    
    def callback_game(self, mtype, repr):
        if mtype == 'app/game+json':
            name = self.obtain(repr['name'], self.callback_name)
            if name:
                game.set_name(name)
            borders = self.obtain(repr['borders'], self.callback_borders)
            if borders:
                game.set_borders(borders)
            
    def callback_name(self, mtype, repr):
        if mtype == 'text/plain':
            game.set_name(repr)
            
    def callback_borders(self, mtype, repr):
        if mtype == 'app/boxlist+json':
            borders = [b for b in repr]
            game.set_borders(borders)   

    def obtain(self, subdata, callback):
        if 'data' in subdata:
            return subdata['data']
        elif 'link' in subdata:
            self.enqueue_request('GET', subdata['link'], [], callback)
            return None
    
    def enqueue_request(self, method, resource, req_args, callback):
        request = (method, resource, req_args, callback)
        self._request_queue.append(request)
        self.send_next_request()
        
    def send_next_request(self):
        if self._pending_rsrc_req is None and self._request_queue:
            method, resource, req_args, cb = self._request_queue[0]
            msg = {'method': method,
                   'resource': resource,
                   'args': req_args
                   }
            self._pending_rsrc_req = resource
            client.do_send(msg)
        
        
client = Client('localhost', 8888)  # connect asynchronously

while not client.connected:
    poll(timeout=0.1)

while client.connected:
    start = time.time()
    client.enqueue_request('GET', '/game/1', [], client.callback_game)
    while not client.in_steady_state():
        poll(timeout=0.1)
    print 'loop millis: %3d' % int((time.time() - start) * 1000)
