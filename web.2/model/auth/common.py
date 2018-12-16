from flask import Flask, jsonify, request, session, escape
from flask_restful import Api, Resource, reqparse
from flask_pymongo import PyMongo, MongoClient
import bcrypt, base64
import numpy
import tensorflow as tf
import requests
import subprocess
import json, wikipediaapi, sys, os, secrets
from flask_socketio import SocketIO, emit
from bson.json_util import loads, dumps
from datetime import datetime

from werkzeug.utils import secure_filename

# For session management
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

# For uploads
CURRENT_DIR = os.getcwd()
UPLOAD_FOLDER = os.path.join(CURRENT_DIR, 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, static_folder='static', static_url_path='')
api = Api(app)

## Configs for token management
# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['json', 'cookies', 'headers']

# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
app.config['JWT_COOKIE_SECURE'] = False

# Disabling cookie expiration, THIS IS A BAD IDEA FOR PROD
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False
app.config['JWT_ACCESS_COOKIE_NAME'] = "access_token"
app.config['JWT_REFRESH_COOKIE_NAME'] = "refresh_token"


# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
# to the refresh endpoint. Technically this is optional, but it is in
# your best interest to not send additional cookies in the request if
# they aren't needed.
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'

# Enable csrf double submit protection. See this for a thorough
# explanation: http://www.redotheweb.com/2015/11/09/api-security.html
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(24)  # Change this!

# client = connect(host='db.1', port=27017)

client = MongoClient("mongodb://db.1:27017")
db = client.IRG
users = db["Users"]
predictions_db = db["Predictions"]

def checkDir(username):
	try:
		os.mkdir(username)
	except FileExistsError:
		pass

def uniqueString(absLength=None):
	min_char = 8
	max_char = 12
	allchar = string.ascii_letters + string.digits
	return "".join(choice(allchar) for x in range(randint(absLength or min_char, absLength or max_char)))

def extractUserPass(self):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help='This parameter needs to be present!', location=['args', 'form', 'json'])
    parser.add_argument('password', required=True, help='This parameter needs to be present!', location=['args', 'form', 'json'])
    args = parser.parse_args()

    username = args['username']
    password = args['password']

    return username, password

def UserExist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True

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

    users.update({
            "Username": username
        },{
            "$set":{
                "last_login": datetime.utcnow()
            }
        })

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

def getToken(user):
    if UserExist(user):
        return users.find({"Username":user})[0]["Tokens"]

def returnAll(username):
    from bson import json_util 
    import json, datetime, pymongo

    if UserExist(username):
        cursor = predictions_db.find({"Username":username}, { "_id": 1, "image": 1, 
                            "predictions": 1, "dateCreated": 1}).sort('dateCreated',pymongo.DESCENDING).limit(20)

        returnJson = json.loads(json_util.dumps(cursor))

        for item in returnJson:
            for k, v in item.items():
                # Edit dictionary to return id instead of _id -> $oid
                if k=="_id":
                    oldId = item[k]['$oid']
                    item['id'] = oldId
                    del item[k]
                # Edit datetime format to look good
                if k=="dateCreated":
                    oldDate = int(item[k]["$date"]) / 1000.0
                    item[k] = datetime.datetime.fromtimestamp(oldDate).strftime('%Y-%m-%d %H:%M:%S')

        return returnJson

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
