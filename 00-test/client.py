from time import sleep
from PodSixNet.Connection2 import Client


class ChatClient(Client):
    def __init__(self, host, port):
        self.pong_received = False
        self.connect((host, port))
        
    def Network_connected(self, data):
        print "Connected to server"
        self.send({"action": "ping"})
        
    def Network_pong(self, data):
        self.pong_received = True
        print 'Received pong'

    def run(self):
        while not self.pong_received:
            self.pump()
            sleep(0.1)
        
        
c = ChatClient('localhost', 8888)
c.run()