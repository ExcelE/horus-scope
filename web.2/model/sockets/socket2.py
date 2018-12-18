from flask_uwsgi_websocket import GeventWebSocket
from model.auth.common import *

websocket = GeventWebSocket(app)

@websocket.route('/ws')
def echo(ws):
    while True:
        msg = ws.receive()
        ws.send(msg)