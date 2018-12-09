from flask import Flask, jsonify, request, session, escape
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt, base64
import numpy
import tensorflow as tf
import requests
import subprocess
import json, wikipediaapi, sys
from flask_socketio import SocketIO, emit

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

def getToken(user):
    if UserExist(user):
        return users.find({"Username":user})[0]["Tokens"]