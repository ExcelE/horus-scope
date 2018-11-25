
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt, base64
import numpy
import tensorflow as tf
import requests
import subprocess
import json, wikipediaapi, sys

app = Flask(__name__, static_folder='static', static_url_path='')
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.IRG
users = db["Users"]

def UserExist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user

        #Get the data
        username = request.form['username']
        password = request.form['password']

        if UserExist(username):
            retJson = {
                'status':301,
                'msg': 'Invalid Username'
            }
            return retJson, 301

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 10
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return retJson, 200

def verifyPw(username, password):
    if not UserExist(username):
        return False

    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def generateReturnDictionary(status, msg):
    retJson = {
        "status": status,
        "msg": msg,
        "status_code": status
    }
    return retJson

def verifyCredentials(username, password):
    if not UserExist(username):
        return generateReturnDictionary(301, "Invalid Username"), True

    correct_pw = verifyPw(username, password)

    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password"), True

    return None, False

def appendWiki(name, prob):
    "Return the wiki of all items."
    if name == "":
        return None

    wiki_wiki = wikipediaapi.Wikipedia('en')
    key = name.split(', ')
    
    retDict = {
        "score": prob,
        "description": key[0]
    }

    page_py = wiki_wiki.page(key[0])
    if page_py.exists():
        retDict["wikipediaUrl"] = page_py.fullurl
        retDict["summary"] = page_py.summary[:256]
    else: 
        return None

    return retDict

class Classify(Resource):
    def post(self):
        #postedData = request.get_json()

        photo = request.files['photo']
        r = photo.save('temp.jpg')
        print("Saved image payload to jpg", file=sys.stderr)
        
        username = request.form['username']
        password = request.form['password']

        retJson, error = verifyCredentials(username, password)
        if error:
            return retJson, retJson['status']

        tokens = users.find({
            "Username":username
        })[0]["Tokens"]

        if tokens<=0:
            return generateReturnDictionary(303, "Not Enough Tokens"), 303

        print("User authenticated!", file=sys.stderr)
        retArray = []
        with open('temp.jpg', 'r') as f:
            proc = subprocess.Popen('python3 label_image.py --image temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            ret = proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                loaded = json.load(g)
                print(g, file=sys.stdout)
                keyLinks = []
                for key in loaded:
                    if loaded[key] > 0.001:
                        retArray.append(appendWiki(key, loaded[key]))

        print("OK: Classified image", file=sys.stderr)
        users.update({
            "Username": username
        },{
            "$set":{
                "Tokens": tokens-1
            }
        })

        print("OK: Tokens docked!", file=sys.stderr)
        return retArray, 200

def getToken(user):
    if UserExist(user):
        return users.find({"Username":user})[0]["Tokens"]
        

class Refill(Resource):
    def post(self):
        
        username = request.form['username']
        password = request.form['password']
        amount = request.form.get('amount', None)

        if amount == None:
            amount = 3

        retJson, error = verifyCredentials(username, password)
        if error:
            return retJson, retJson['status']

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
            "new total": currAmount
        }

        return respJson, 200


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
        
        print("No errors here", file=sys.stderr)
        response = generateReturnDictionary(200, "Success")
        return response, 200

## Serving static files
@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory('static', path)


api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)
