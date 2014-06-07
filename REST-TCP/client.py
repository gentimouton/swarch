from network import Handler, poll_for, poll
import time
from collections import deque

TICK_DURATION = 0.02  # seconds

sent = False
name = None
borders = None
pellets = None
players = None

class Client(Handler):
    
    request_queue = deque() # queue of resources to request
    
    def on_msg(self, data):
        request = self.request_queue.popleft()
        mtype, repr = data['type'], data['representation']
        global name, borders, pellets, players
        if mtype == 'app/game+json':
            name = self.obtain(repr['name'])
            borders = self.obtain(repr['borders'])
        elif mtype == 'app/boxlist+json':
            # TODO: how do I know if it's borders, pellets, or players??
            pass
        self.send_next_request()

    def obtain(self, subdata):
        if 'data' in subdata:
            return subdata['data']
        elif 'link' in subdata:
            self.enqueue_request('GET', subdata['link'], [])
            return None
            
    def enqueue_request(self, method, resource, args):
        request = (method, resource, args)
        self.request_queue.append(request)
        
    def send_next_request(self):
        if self.request_queue:
            method, resource, args = self.request_queue[0]
            msg = {'method': method,
                   'resource': resource,
                   'args': args
                   }
            client.do_send(msg)
        else:
            print 'Warning: no more requests to send to the server!'

        
client = Client('localhost', 8888)  # connect asynchronously

while not client.connected:
    poll(0.01)

client.enqueue_request('GET', '/game/1', [])
client.send_next_request()

while client.connected:
    loop_start = time.time()
    poll_for(TICK_DURATION - (time.time() - loop_start)) # poll until tick is over
