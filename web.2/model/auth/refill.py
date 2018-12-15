from .common import *

class Refill(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()
        amount = request.form['amount'] or 3

        amount = int(amount)
        
        currAmount = getToken(username)
        newAmount = currAmount + amount

        users.update({
            "Username": username
        },{
            "$set":{
                "Tokens": newAmount
            }
        })

        respJson = {
            "status": 200,
            "msg": "Refilled",
            "requested": amount,
            "new total": newAmount
        }

        return respJson, 200