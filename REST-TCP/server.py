import json
from network import Listener, Handler, poll
import sqlite3
from random import randint

HOST_NAME = 'localhost'  
PORT_NUMBER = 8888
SALT = 'secret salt'  # protects from dictionary attacks

class DB:
    
    def __init__(self):
        self._conn = sqlite3.connect('whale.sqlite3')
        self._cur = self._conn.cursor()
        # TODO: add expiration timestamp to the players table
        self.execute('''
            CREATE TABLE IF NOT EXISTS players
            (url TEXT, name TEXT, x INT, y INT, size INT, 
            PRIMARY KEY (url, name) );
            ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS pellets 
            (id INTEGER PRIMARY KEY, x INT, y INT, size INT);
            ''')
        for pid in range(4):
            try:
                q = 'INSERT OR ABORT INTO pellets VALUES (?, ?, ?, ?);'
                args = pid, randint(10, 380), randint(10, 280), 5
                self.execute(q, args)
            except sqlite3.IntegrityError:
                # primary key conflict: row already exists
                pass
    
    def execute(self, q, args=()):
        return self._cur.execute(q, args)
        
    def commit(self):
        self._conn.commit()
    
    def close(self):
        self._conn.close()
        
db = DB()


input_map = {'up': (0, -5), 'down': (0, 5), 'left': (-5, 0), 'right': (5, 0)}
borders = [ [0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2] ]
def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1


def get_game(args):
    repr = {'borders': {'link': '/borders'},
            'pellets': {'link': '/pellets'},
            'players': {'link': '/players'}
            }
    if 'name' in args:  # TODO: clients know to submit their name from /login
        name = args['name']  # TODO: also add password detection
        q = 'SELECT name, url FROM players'
        players = db.execute(q).fetchall()
        name2url = {p[0]: p[1] for p in players}
        if name in name2url:
            url = name2url[name]
        else:
            url = '/player/' + str(hash(name + SALT))
            q = '''INSERT INTO players(url, name, x, y, size) 
                    VALUES (?, ?, ?, ?, ?);'''
            qargs = url, name, randint(10, 380), randint(10, 280), 10
            db.execute(q, qargs)
            db.commit()
        repr['you'] = {'form': {'method': 'POST',
                                'url': url,
                                'args': ['direction']
                                }
                       }
    return 'app/game+json', repr
    
def get_borders(args):
    # borders are static, can be cached, no need to store them in DB
    return 'app/boxlist+json', borders

def get_pellets(args):
    # pellets may change, fetch them from DB
    q = 'SELECT x, y, size FROM pellets;'
    pellets = db.execute(q).fetchall()
    box_list = [ [p[0], p[1], p[2], p[2]] for p in pellets]
    return 'app/boxlist+json', box_list

def get_players(args):
    # players always change, fetch them from DB
    q = 'SELECT name, x, y, size, url FROM players;'
    players = db.execute(q).fetchall()
    box_dict = { p[0]: [p[1], p[2], p[3], p[3]] for p in players}
    return 'app/boxdict+json', box_dict

def post_player(url, args):
    # TODO: detect collisions with other players
    q = 'SELECT name, x, y, size FROM players WHERE url = ?;'
    qargs = (url,)
    row = db.execute(q, qargs).fetchone()
    if not row:
        return 'text/plain', 'Wrong URL'
    name, x, y, size = row
    if 'direction' not in args:
        return 'text/plain', 'Need direction argument'
    dx, dy = input_map[args['direction']]
    box = [x + dx, y + dy, size, size]
    # collision with pellets
    q = 'SELECT id, x, y, size FROM pellets;'
    pellets = db.execute(q).fetchall()
    for pellet in pellets:
        pid, px, py, psize = pellet
        if collide_boxes(box, [px, py, psize, psize]):
            box = [box[0], box[1], box[2] * 1.2, box[3] * 1.2]  # grow
            q = '''UPDATE pellets SET x = ?, y = ?, size = ? 
                    WHERE id = ?;'''
            qargs = randint(10, 380), randint(10, 280), 5, pid 
            db.execute(q, qargs)
            db.commit()
    # collision with borders
    col_brdr = any([collide_boxes(box, brdr) for brdr in borders])
    if col_brdr:
        box = [randint(10, 380), randint(10, 280), 10, 10]
    q = 'UPDATE players SET x = ?, y = ?, size = ? WHERE url = ?;'
    qargs = box[0], box[1], box[2], url
    db.execute(q, qargs)
    db.commit()
    return 'app/boxdict+json', {name: box}
    
    


class MyHandler(Handler):
    
    def on_msg(self, req):
        method = req['method']
        resource = req['resource']
        args = req['args']
        if (method, resource) == ('GET', '/game/1'):
            mtype, repr = get_game(args)
        elif (method, resource) == ('GET', '/borders'):
            mtype, repr = get_borders(args)
        elif (method, resource) == ('GET', '/pellets'):
            mtype, repr = get_pellets(args)
        elif (method, resource) == ('GET', '/players'):
            mtype, repr = get_players(args)
        elif method == 'POST' and resource.startswith('/player/'):
            mtype, repr = post_player(resource, args)
        else:  # invalid resource 
            mtype, repr = 'text/plain', 'Wrong resource or method.\nGo to /'
        response = {'resource': resource,
                    'type': mtype,
                    'representation': repr
                    }
        self.do_send(response)

        
if __name__ == '__main__':
    server = Listener(8888, MyHandler)
    try:
        while 1:
            poll()
    except KeyboardInterrupt:
        db.close()    
