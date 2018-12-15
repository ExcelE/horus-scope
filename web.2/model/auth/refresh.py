'''
    This is required for refreshing token management.
'''

from .common import *

class Refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        # Create the new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        # Set the access JWT and CSRF double submit protection cookies
        # in this response
        resp = jsonify({'refresh': True})
        resp.status_code = 200
        set_access_cookies(resp, access_token)
        return resp