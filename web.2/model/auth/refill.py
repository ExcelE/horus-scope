from .common import *

class Refill(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()

        amount = 3
        
        currAmount = getToken(username)
        newAmount = currAmount + amount

        users.update({
            "Username": username
        },{
            "$set":{
                "credits": newAmount
            }
        })

        respJson = {
            "status": 200,
            "msg": "Refilled",
            "credits": newAmount
        }

        return respJson, 200