from .common import *

class Logout(Resource):
    def post(self):
        if 'username' in session:
            retJson = {}
            
            username = escape(session['username'])

            retJson.tokens = getToken(username)