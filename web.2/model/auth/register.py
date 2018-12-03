from .common import *

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user

        #Get the data
        print(request, file=sys.stderr)
        try:
            username = request.get_json()['username']
            password = request.get_json()['password']
        except Exception as e:
            username = request.form['username']
            password = request.form['password']
        except:
            return generateReturnDictionary(305, "Please validate body format"), 305

        if UserExist(username):
            retJson = generateReturnDictionary(301, "Invalid username")
            return retJson, 301

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        print("Password encrypted and stored", file=sys.stderr)
        #Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 10
        })

        retJson = generateReturnDictionary(200, "Successfully signed up!")
        session['username'] = username
        retJson.set_cookie('username', username)

        return retJson, 200