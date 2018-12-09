from .common import *

class Logout(Resource):
    def post(self):
        session.pop('username', None)