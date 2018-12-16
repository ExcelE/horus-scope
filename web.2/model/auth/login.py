from .common import *

class Login(Resource):
    def post(self):
        
        username, password = extractUserPass(request)

        retJson, err = verifyCredentials(username, password)
        if err:
            print("Sending unknown username/pass error", file=sys.stderr)
            return retJson, retJson['status']

         # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        response = jsonify({
            'login': True,
            'access_token': access_token,
            # 'refresh_token': refresh_token
            })

        response.status_code = 200

        # Embedding cookies
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response

    @jwt_required
    def get(self):
        username = get_jwt_identity()
        tokens_available = getToken(username)
        history = returnAll(username)
        return {
            "msg": history,
            "credits": tokens_available
        }, 200