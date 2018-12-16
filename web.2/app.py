from model.auth.register import Register
from model.auth.login import Login
from model.auth.logout import Logout
from model.auth.refill import Refill
from model.classify import Classify
from model.auth.common import *
from model.auth.refresh import Refresh
from model.auth.uploads import Uploads
from model.auth.delete import Delete

# Do not use in Production
app.secret_key = secrets.token_urlsafe(24)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
checkDir(app.config['UPLOAD_FOLDER'])

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')
api.add_resource(Refresh, '/refresh')
api.add_resource(Delete, '/delete')
api.add_resource(Uploads, '/uploads/<path:filename>')

jwt = JWTManager(app)

from flask_sockets import Sockets
sockets = Sockets(app)

@sockets.route('/ws')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__=="__main__":
    app.debug = True
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # app.run(debug=True, host='0.0.0.0')
