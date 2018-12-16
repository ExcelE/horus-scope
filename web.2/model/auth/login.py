from .common import *
from datetime import datetime

class Login(Resource):
    def post(self):
        
        username, password = extractUserPass(request)

        retJson, err = verifyCredentials(username, password)
        if err:
            return retJson, retJson['status']

         # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        tokens_available = getToken(username)
        history = returnAll(username)

        last_login = users.find_one({"Username": username})["last_login"]

        response = jsonify({
            'history': history,
            'access_token': access_token,
            "credits": tokens_available,
            "last_login": last_login
            })

        response.status_code = 200

        # Embedding cookies
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response

    @jwt_required
    def get(self):
        username = get_jwt_identity()
        last_login = users.find_one({"Username": username})["last_login"]
        tokens_available = getToken(username)
        history = returnAll(username)

        return {
            "last_login": last_login,
            "history": history,
            "credits": tokens_available
        }, 200