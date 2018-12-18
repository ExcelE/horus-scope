from model.auth.register import Register
from model.auth.login import Login
from model.auth.logout import Logout
from model.auth.refill import Refill
from model.classify import Classify
from model.auth.common import *
from model.auth.refresh import Refresh
from model.auth.uploads import Uploads
from model.auth.delete import Delete
from model.auth.profile import Profile

sys.path.append('../..')

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
api.add_resource(Profile, '/profile')
api.add_resource(Uploads, '/uploads/<path:filename>')

jwt = JWTManager(app)

### SOCKET
from flask_socketio import Namespace, emit, SocketIO
socketio = SocketIO(app)

class MyCustomNamespace(Namespace):
    def on_connect(self):
        emit('my_response', data)

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        emit('my_response', data)

socketio.on_namespace(MyCustomNamespace('/ws'))
### END SOCKET

if __name__=="__main__":
    import os

    app.run(debug=os.environ.get("DEBUG", default = 0),
            host='0.0.0.0', gevent=100)

    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    # server.serve_forever()
