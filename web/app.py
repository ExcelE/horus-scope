from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt, base64
import numpy
import tensorflow as tf
import requests
import subprocess
import json, wikipediaapi

app = Flask(__name__)
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
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"

        if UserExist(username):
            retJson = {
                'status':301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens":10
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

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
        "msg": msg
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
        "prob": prob
    }

    for item in key:
        page_py = wiki_wiki.page(item)
        if page_py.exists():
            retDict[item] = page_py.fullurl
        else: 
            retDict[item] = ""

    return retDict

class Classify(Resource):
    def post(self):
        postedData = request.get_json()
        url = postedData[0]

        # username = postedData["username"]
        # password = postedData["password"]

        # retJson, error = verifyCredentials(username, password)
        # if error:
        #     return jsonify(retJson)

        # tokens = users.find({
        #     "Username":username
        # })[0]["Tokens"]

        # if tokens<=0:
        #     return jsonify(generateReturnDictionary(303, "Not Enough Tokens"))

        r = base64.b64decode(url)
        retJson = {}
        with open('temp.jpg', 'wb') as f:
            f.write(r)
            proc = subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            ret = proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                retJson = json.load(g)
                keyLinks = {}
                for key in retJson:
                    if retJson[key] > 0.001:
                        keyLinks[key] = appendWiki(key, retJson[key])
                retJson = keyLinks

        # users.update({
        #     "Username": username
        # },{
        #     "$set":{
        #         "Tokens": tokens-1
        #     }
        # })

        retJson["status"] = 200

        return retJson


class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        amount = postedData["amount"]

        if not UserExist(username):
            return jsonify(generateReturnDictionary(301, "Invalid Username"))

        correct_pw = "abc123"
        if not password == correct_pw:
            return jsonify(generateReturnDictionary(302, "Incorrect Password"))

        users.update({
            "Username": username
        },{
            "$set":{
                "Tokens": amount
            }
        })
        return jsonify(generateReturnDictionary(200, "Refilled"))


api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__=="__main__":
    app.run(host='0.0.0.0')
