from .common import *

class Refill(Resource):
    def post(self):
        if 'username' in session:
            amount = request.form.get('amount', None)

            if amount == None:
                amount = 3
            else: 
                amount = int(amount)

            username = escape(session['username'])
            
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

        else:
            resp = generateReturnDictionary(300, "Please log in first!")
            return resp, 300