"""
REST constraints: 
- client-server, 
- layered, 
- stateless interactions: client stores app state, server stores resource state,
- uniform interface, 
- caching (optional), 
- code on demand (optional).

See:
http://stackoverflow.com/a/671132/856897
http://roy.gbiv.com/talks/200804_REST_ApacheCon.pdf

Uniform interface can be broken down into the following constraints:
- Each resource (= information) has one name: its URI.
- Resource-generic interaction semantics (same verbs work on all resources)
- Manipulate resources through their representations.
- Hypermedia as the engine of application state: need links between resources.

I want to use JSON as a representation+links format.
Even though there is no right way to link resources in JSON,
I'm using Content-type: application/hal+json.
http://stateless.co/hal_specification.html
https://www.mnot.net/blog/2011/11/25/linking_in_json


TODO: also provide XML or HTML representations (not just JSON).
TODO: make a TCP version instead of HTTP

"""
import BaseHTTPServer
import json
import sqlite3


HOST_NAME = 'localhost'  
PORT_NUMBER = 8888

db_conn = sqlite3.connect('whale.sqlite3')
db_cursor = db_conn.cursor()
db_cursor.execute('''CREATE TABLE IF NOT EXISTS players 
                (name TEXT, x REAL, y REAL, size REAL)''')
db_cursor.execute('''CREATE TABLE IF NOT EXISTS pellets 
                (id INT, x REAL, y REAL, size REAL)''')
db_cursor.execute('''INSERT INTO PELLETS VALUES(1, 200, 200, 10)''')
db_conn.commit()

# Borders are static. No need to store them in a database. Cache them here.
# Map resource URI to representation for the 4 borders.
borders = {'/border/1': [0, 0, 2, 300],
           '/border/2': [0, 0, 400, 2],
           '/border/3': [398, 0, 2, 300],
           '/border/4': [0, 298, 400, 2] }

# pellets and player positions change often
pellets = {'/pellet/1': []
           }

# map resource to representation
def representation(resource):
    if ressource == '/':
        return  {'borders': [{'href': b} for b in borders.keys()]}
    elif resource == '/border/1':
        return [0, 0, 2, 300]
    elif resource == '/border/2':
        return [0, 0, 400, 2]
    elif resource == '/border/3':
        return [398, 0, 2, 300]
    elif resource == '/border/4':
        return [0, 298, 400, 2]
    elif resource == '/pellet/1':
        return []
         


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        # don't log messages in stderr
        pass
     
    def send_reply(self, code, headers, body):
        BaseHTTPServer.BaseHTTPRequestHandler.send_response(self, code)
        [self.send_header(k, v) for k, v in headers.items()]
        self.end_headers()
        self.wfile.write(json.dumps(body))
    
    def do_HEAD(self):
        # TODO: borders never change, pellets rarely, players often 
        pass
            
    def do_GET(self):
        uri = self.path
        headers = {"Content-type": "application/json+whale"}
        if uri == '/':  # root
            code = 200
            msg = {'borders': [{'href': b} for b in borders.keys()]}
        elif uri in borders.keys():
            code = 200
            msg = borders[uri]
        elif uri in pellets.keys():
            code = 200
        else:
            code = 404
            msg = 'Bad URI'
        self.send_reply(code, headers, msg)

            
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_DELETE(self):
        pass
    
    def do_PUT(self):
        pass
        
if __name__ == '__main__':
    server = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    db_conn.close()


    
