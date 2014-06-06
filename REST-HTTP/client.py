""" 
Borders are static. Clients should cache them once they GET them.

TODO: run 2 HTTP servers, on 8888 and 8889. 
Highlight web server's replaceability. 
""" 
import httplib
import json


HOST_NAME = '127.0.0.1'  # 'localhost' lags: http://bugs.python.org/issue6085
PORT_NUMBER = 8888

conn = httplib.HTTPConnection(HOST_NAME, PORT_NUMBER)

conn.request('GET', '/')
response = conn.getresponse()  # response.status, response.reason is 200, 'OK'
data = json.loads(response.read())


for border in data['borders']:
    conn.request('GET', border['href'])
    response = conn.getresponse()
    data2 = json.loads(response.read())


conn.close()



