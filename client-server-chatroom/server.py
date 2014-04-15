from network import Listener, Handler, poll
from time import sleep


handlers = {}  # map client handler to user name

class MyHandler(Handler):
    
    def on_open(self):
        pass
        
    def on_close(self):
        pass
    
    def on_msg(self, msg):
        print msg
    
class Serv(Listener):
    handlerClass = MyHandler


port = 8888
server = Serv(port)
while 1:
    poll()
    sleep(0.05)  # seconds

