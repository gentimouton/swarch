import json
from network import Listener, Handler, poll
import sqlite3
from random import randint

HOST_NAME = 'localhost'  
PORT_NUMBER = 8888
SALT = 'secret salt'

db_conn = sqlite3.connect('whale.sqlite3')
db_cur = db_conn.cursor()
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS players
    (url TEXT, name TEXT, x INT, y INT, size INT, PRIMARY KEY (url, name));
    ''')
# TODO: also add an expiration timestamp
db_cur.execute('''
    CREATE TABLE IF NOT EXISTS pellets 
    (id INTEGER PRIMARY KEY, x INT, y INT, size INT);
    ''')
for pellet_id in range(4):
    try:
        db_cur.execute('''
            INSERT OR ABORT INTO pellets VALUES (?, ?, ?, ?);
            ''', (pellet_id, randint(10, 380), randint(10, 280), 5))
    except sqlite3.IntegrityError:  # primary key conflict: row already exists
        pass
db_conn.commit()



input_map = {'up': (0, -5), 'down': (0, 5), 'left': (-5, 0), 'right': (5, 0)}
borders = [ [0, 0, 2, 300], [0, 0, 400, 2], [398, 0, 2, 300], [0, 298, 400, 2] ]
def collide_boxes(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return x1 < x2 + w2 and y1 < y2 + h2 and x2 < x1 + w1 and y2 < y1 + h1


class MyHandler(Handler):
    
    def on_msg(self, req):
        method = req['method']
        resource = req['resource']
        args = req['args']
        if (method, resource) == ('GET', '/game/1'):
            repr = {'borders': {'link': '/borders'},
                    'pellets': {'link': '/pellets'},
                    'players': {'link': '/players'}
                    }
            if 'name' in args:  # TODO: how do clients know to submit their name?
                name = args['name']  # TODO: also add password detection
                players = db_cur.execute('''
                    SELECT name, url FROM players
                    ''').fetchall()
                name2url = {p[0]: p[1] for p in players}
                if name in name2url:
                    url = name2url[name]
                else:
                    url = '/player/' + str(hash(name + SALT))
                    db_cur.execute('''
                        INSERT INTO players(url, name, x, y, size) 
                        VALUES (?, ?, ?, ?, ?);
                        ''', (url, name, 150, 150, 10))  # start position
                    db_conn.commit()
                repr['you'] = {'form': {'method': 'POST',
                                        'url': url,
                                        'args': ['dir']}
                               }
            response = {'resource': resource,
                        'type': 'app/game+json',
                        'representation': repr
                        }
        elif (method, resource) == ('GET', '/borders'):
            # borders are static, can be cached, no need to store them in DB
            repr = borders
            response = {'resource': resource,
                        'type': 'app/boxlist+json',
                        'representation': repr
                        }
        elif (method, resource) == ('GET', '/pellets'):
            # pellets may change, fetch them from DB
            pellets = db_cur.execute('''
                SELECT x, y, size FROM pellets;
                ''').fetchall()
            repr = [ [p[0], p[1], p[2], p[2]] for p in pellets]
            response = {'resource': resource,
                        'type': 'app/boxlist+json',
                        'representation': repr
                        }
        elif (method, resource) == ('GET', '/players'):
            # players always change, fetch them from DB
            players = db_cur.execute('''
                SELECT name, x, y, size, url FROM players;
                ''').fetchall()
            box_dict = { p[0]: [p[1], p[2], p[3], p[3]] for p in players}
            response = {'resource': resource,
                        'type': 'app/boxdict+json',
                        'representation': box_dict
                        }
        elif method == 'POST' and resource.startswith('/player/'):
            if 'dir' in args:
                d = args['dir']
                dx, dy = input_map[d]
                # TODO: detect collisions with borders, pellets, and players
                name, x, y, size = db_cur.execute('''
                    SELECT name, x, y, size FROM players WHERE url = ?;
                    ''', (resource,)).fetchone()
                box = [x + dx, y + dy, size, size]
                # collision with pellets
                pellets = db_cur.execute('''
                    SELECT id, x, y, size FROM pellets;
                    ''').fetchall()
                for pellet in pellets:
                    pid, px, py, psize = pellet
                    if collide_boxes(box, [px, py, psize, psize]):
                        box = [box[0], box[1], box[2] * 1.2, box[3] * 1.2]
                        db_cur.execute('''
                            UPDATE pellets SET x = ?, y = ?, size = ?
                            WHERE id = ?;
                            ''', (randint(10, 380), randint(10, 280), 5, pid))
                        db_conn.commit()
                # collision with borders
                col_brdr = any([collide_boxes(box, brdr) for brdr in borders])
                if col_brdr:
                    box = [150, 150, 10, 10]
                db_cur.execute('''
                    UPDATE players SET x = ?, y = ?, size = ? WHERE url = ?;
                    ''', (box[0], box[1], box[2], resource))
                db_conn.commit()
            box_dict = { name: box}
            response = {'resource': resource,
                        'type': 'app/boxdict+json',
                        'representation': box_dict
                        }
        else:  # invalid resource 
            response = {'resource': resource,
                        'type': 'text/plain',
                        'representation': 'wrong resource or method.\nGo to /'
                        }
        
        self.do_send(response)

    
    
        
if __name__ == '__main__':
    server = Listener(8888, MyHandler)
    try:
        while 1:
            poll()
    except KeyboardInterrupt:
        db_conn.close()    
