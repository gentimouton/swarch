from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from time import sleep

class ClientChannel(Channel):
        
    def Close(self):
        print 'Disconnection from: %s' % (str(self.addr))
    
    def Network_ping(self, data):
        print 'Ping by: %s' % (str(self.addr))
        self.Send({'action': 'pong'})
        
    
class ChatServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, host, port):
        Server.__init__(self, localaddr=(host, port))
        print 'Server running at %s:%d' % (host, port)
    
    def Connected(self, channel, addr):
        print 'Connection from: %s' % (str(addr))
        
    def run(self):
        while True:
            self.Pump()
            sleep(0.1)


s = ChatServer('localhost', 8888)
s.run()
