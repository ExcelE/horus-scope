from .common import *

class Register(Resource):
    def post(self):

        username, password = extractUserPass(request)

        if UserExist(username):
            return generateReturnDictionary(301, "Username not available"), 301

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        users.insert({
             "Username": username,
             "Password": hashed_pw,
             "Tokens":10
        })

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
        