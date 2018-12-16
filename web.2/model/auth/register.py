from .common import *

class Register(Resource):
    def post(self):

        # parser = reqparse.RequestParser()
        # parser.add_argument('username', required=True, help='This parameter needs to be present!', location=['args', 'form', 'json'])
        # parser.add_argument('password', required=True, help='This parameter needs to be present!', location=['args', 'form', 'json'])
        # args = parser.parse_args()

        username, password = extractUserPass(request)

        if UserExist(username):
            return generateReturnDictionary(301, "Username not available"), 301

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        initialCredits = 10

        users.insert({
             "Username": username,
             "Password": hashed_pw,
             "Tokens": initialCredits
        })

        users.update({"Username": username},
        {
            "$set": {
                "last_login": datetime.utcnow()
            }
        })

        response = jsonify({
            'login': True,
            'access_token': access_token,
            'credits': initialCredits
        })

        response.status_code = 200

        # Embedding cookies
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response
        