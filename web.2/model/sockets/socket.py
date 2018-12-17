from flask_sockets import Sockets
from model.auth.common import *
sockets = Sockets(app)

@sockets.route('/ws')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

@app.route('/')
def hello():
    return 'Hello World!'
