from .common import *

class Register(Resource):
    def post(self):
        try:
            username = request.form['username']
            password = request.form['password']
        except:
            username = request.get_json()['username']
            password = request.get_json()['password']

        if UserExist(username):
            return generateReturnDictionary(301, "Username not available"), 301

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 10
        })

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