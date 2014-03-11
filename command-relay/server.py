from time import sleep
from network import Listener, Handler, poll

handlers = set()
def broadcast(msg):
    copies = handlers.copy()  # avoid "Set changed size during iteration" error
    [h.do_send(msg) for h in copies]

class MyHandler(Handler):
        
    def on_open(self):
        self.myname = ''
        handlers.add(self)
        
    def on_close(self):
        handlers.remove(self)
        broadcast({'msgtype': 'leave', 'name': self.myname})
        
    def on_msg(self, data):
        msgtype = data['msgtype']
        name = data['name']
        if msgtype == 'join':  # the player joined: forward his/her name
            self.myname = name
            broadcast({'msgtype': 'join', 'name': name})
        elif msgtype == 'move':
            top, left = data['top'], data['left']
            broadcast({'msgtype': 'move', 'name': name,
                       'top': top, 'left': left})
              
class Server(Listener):
    handlerClass = MyHandler
    
server = Server(8888)
while 1:
    poll()
    sleep(.05)  # 50ms, 20 frames per second
