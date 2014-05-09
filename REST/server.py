"""

"""
import BaseHTTPServer
import json
import sqlite3


HOST_NAME = 'localhost'  # 'localhost' lags: http://bugs.python.org/issue6085
PORT_NUMBER = 8888

db_conn = sqlite3.connect('whale.sqlite3')
db_cursor = db_conn.cursor()
db_cursor.execute('''CREATE TABLE IF NOT EXISTS players 
                (name text, x real, y real, size real)''')
db_cursor.execute('''CREATE TABLE IF NOT EXISTS pellets 
                (id int, x real, y real, size real)''')
db_conn.commit()

# Borders are static. No need to store them in a database. 
# Map resource to representation for the 4 borders.
borders = {'/border/1': [0, 0, 2, 300],
           '/border/2': [0, 0, 400, 2],
           '/border/3': [398, 0, 2, 300],
           '/border/4': [0, 298, 400, 2] }

        
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
        # TODO: /borders never changes
        pass
            
    def do_GET(self):
        # / for game state
        resource = self.path
        headers = {"Content-type": "application/json"}
        if resource == '/':
            code = 200
            msg = {'borders': borders.keys()}
        elif resource in borders.keys():
            code = 200
            msg = borders[resource]
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


    
