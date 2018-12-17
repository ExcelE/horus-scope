from .common import *

class Profile(Resource):
    # Have the user save their profile info
    # Params: email, About Me section,
    @jwt_required
    def post(self):
        username = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('email', help="User's preferred email.", location=['form', 'json'])
        parser.add_argument('aboutMe', help="User's about me section.", location=['form', 'json'])
        args = parser.parse_args()

        userEmail = args["email"]
        userAboutMe = args["aboutMe"]

        if (not userEmail and not userAboutMe):
            return {"msg": "Please specify something to modify. Otherwise, use GET on this endpoint."}, 400

        currentUser = {"Username": username}

        try:
            updateValues = {
                "$set": {
                    "email": "" if userEmail is None else userEmail, 
                    "aboutMe": "" if userAboutMe is None else userAboutMe,
                    "lastUpdated": datetime.utcnow()
                    }
            }

            # Update the user info in database
            users.update_one(currentUser, updateValues)
            return {"msg": "User profile updated!"}, 200

        except:
            return {"msg": "Something went wrong! Try again later."}, 400
    
    # Return user profile info/settings
    @jwt_required
    def get(self):
        from bson import json_util 
        import json
        username = get_jwt_identity()

        cursor = users.find_one({"Username":username}, {"_id": 0,"credits": 1, "Username": 1, "last_login": 1, "aboutMe": 1, "email": 1})

        returnJson = json.loads(json_util.dumps(cursor))

        oldDate = int(returnJson["last_login"]["$date"]) / 1000.0
        returnJson["lastLogin"] = datetime.fromtimestamp(oldDate).strftime('%Y-%m-%d %H:%M:%S UTC')
        del returnJson["last_login"]

        return returnJson, 200
