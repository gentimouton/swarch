"""
A client connection that sends to and receives from the server.
Inspired by PodSixNet's Connection module.
Subclasses of Client must have methods like Network_myaction 
to receive server messages about myaction.
"""

from EndPoint import EndPoint

class Client:

    def connect(self, host, port):
        self.endpoint = EndPoint()
        self.endpoint.DoConnect((host, port))
        # check for connection errors:
        self.pump()
    
    def pump(self):
        self.endpoint.Pump() # send data to server
        for data in self.endpoint.GetQueue(): # invoke callbacks
            for n in ("Network_" + data['action'], "Network"):
                if hasattr(self, n):
                    getattr(self, n)(data)
    
    def send(self, data):
        self.endpoint.Send(data)
