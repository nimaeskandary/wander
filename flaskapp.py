#!/usr/bin/env python3
# Morgan Wallace
# 2017

from flask import Flask, make_response, jsonify, request, abort, current_app
from flask_pymongo import PyMongo
import json
from bson import ObjectId
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
import routehelper as rh

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)
cors = CORS(app)

app.config['MONGO_DBNAME'] = 'groups'
groupClient = PyMongo(app, config_prefix='MONGO')

auth = HTTPBasicAuth()

"""
Routes:
/                                       GET     home_page()
/joinGroup/<groupCode>                  POST    joinGroup(groupCode)
/createGroup                            POST    createGroup()
/updateLoc                              POST    updateLoc()
/groupUpdate/<groupCode>                GET     groupUpdate(groupCode)
/groupEnd/<groupCode>                   GET     groupEnd(groupEnd)
"""
#@app.after_request
#def after_request(response):
#    return rh.after_request(app, clients, response)
@app.errorhandler(404)
@cross_origin()
def not_found(error):
    return rh.not_found(app, groupClient, error)

# Home Page (unused)
@app.route('/', methods=['GET', 'OPTIONS'])
@cross_origin()
def home_page():
    return rh.home_page(app, groupClient)

# Join group
@app.route('/joinGroup/<groupCode>', methods=['POST'])
@cross_origin()
def joinGroup(groupCode):
    return rh.joinGroup(app, groupClient, groupCode)

# Create group
@app.route('/createGroup',methods=['POST'])
@cross_origin()
def createGroup():
    return rh.createGroup(app, groupClient)

####EXAMPLE####
# Send an updated practical
# Creates new user if none existing for that PERNR
@app.route('/agents/<PERNR>/practicals/<practical>', methods=['POST'])
@cross_origin()
def save_practical(PERNR, practical):
    return rh.save_practical(app, clients, PERNR, practical)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
