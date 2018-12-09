from .common import *

class Login(Resource):
    def post(self):
        try:
            username = request.form["username"]
            password = request.form["password"]
            print("Correct request params", file=sys.stderr)
        except:
            response = generateReturnDictionary(300, "Invalid user/pass format.")
            print("Invalid user/pass", file=sys.stderr)
            return response, 300

        retJson, err = verifyCredentials(username, password)
        if err:
            print("Sending unknown username/pass error", file=sys.stderr)
            return retJson, retJson['status']

        session['username'] = username
        response = generateReturnDictionary(200, "Success")

        return response, 200