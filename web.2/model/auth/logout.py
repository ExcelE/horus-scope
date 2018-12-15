from .common import *

class Logout(Resource):
    def post(self):
        resp = jsonify({'logout': True})
        resp.status_code = 200
        unset_jwt_cookies(resp)
        return resp