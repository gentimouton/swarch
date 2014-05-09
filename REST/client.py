""" 
Borders are static. Clients should cache them once they GET them.
""" 
import httplib
import json


HOST_NAME = '127.0.0.1'
PORT_NUMBER = 8888

conn = httplib.HTTPConnection(HOST_NAME, PORT_NUMBER)

conn.request('GET', '/')
response = conn.getresponse()  # response.status, response.reason is 200, 'OK'
data = json.loads(response.read())


for uri in data['borders']:
    conn.request('GET', uri)
    response = conn.getresponse()
    data2 = json.loads(response.read())

conn.close()

