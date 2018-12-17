from flask_uwsgi_websocket import GeventWebSocket

websocket = GeventWebSocket(app)

@websocket.route('/echo')
def echo(ws):
    while True:
        msg = ws.receive()
        ws.send(msg)