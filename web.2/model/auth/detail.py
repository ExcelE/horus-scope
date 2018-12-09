from .common import *

class Details(Resource):
    def post(self):
        if 'username' in session:
            retJson = {}
            
            username = escape(session['username'])

            retJson.tokens = getToken(username)