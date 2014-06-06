from network import Handler, poll_for, poll
import time


TICK_DURATION = 0.02  # seconds

sent = False
    
class Client(Handler):
            
    def on_msg(self, data):
        print data
        self.do_close()
        
client = Client('localhost', 8888)  # connect asynchronously

while not client.connected:
    poll(0.01)
msg = {'resource': '/auth', 
       'method': 'CREATE'
       }
client.do_send(msg)

while 1:
    loop_start = time.time()
    poll_for(TICK_DURATION - (time.time() - loop_start)) # poll until tick is over
