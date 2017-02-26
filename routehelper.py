#!/usr/bin/env python3
# Morgan Wallace
# 2017
import random, math, string
from flask import Flask, make_response, jsonify, request, abort, current_app
from flask_pymongo import PyMongo
import json
from bson import ObjectId
from flask_cors import CORS

def after_request(app, client, response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def not_found(app, client, error):
    return make_response(jsonify({'error': "Not Found"}), 404)

def home_page(app, client):
    if request.json:
        return jsonify(request.json), 200
    else:
        return jsonify({'response': "This is the home page for wander; please make a specific request"}), 200

def joinGroup(app, groupClient, groupCode):
    if not request.json or not ("dispName" in request.json):
        abort(400) # Bad request
    #Validate group code in MONGO
    if (not (groupCode.upper() in groupClient.db.collection_names())):
        abort(404)
    #Add member to group in MONGO
    group = groupClient.db[groupCode.upper()].find()
    if group.count() > 1: #too many listings or none (should not be encountered)
        abort(400)
    doc = group.next()
    user = {}
    user["dispName"] = request.json["dispName"]
    user["level"] = "m"
    user["location"] = []
    memberList = doc["memberList"]
    memberList.append(user)
    doc["memberList"] = memberList
    result = groupClient.db[groupCode.upper()].replace_one({"groupName": doc["groupName"]},doc)
    #Return 200
    return 200

def createGroup(app, groupClient):
    if not request.json or not all(key in request.json for key in ("groupName","dispName","triggerDist")):
        abort(400) # Bad request
    #Generate group code & validate not existing
    d = {}
    d["groupCode"] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
    while d["groupCode"] in groupClient.db.collection_names():
        d["groupCode"] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
    #Create new Mongo document entry & add member to group
    doc = {}
    doc["groupCode"] = d["groupCode"]
    doc["groupName"] = request.json["groupName"]
    doc["triggerDist"] = request.json["triggerDist"]
    if ("lostMessage" in request.json):
        doc["lostMessage"] = request.json["lostMessage"]
    else:
        doc["lostMessage"] = "You've been separated from your group!"
    memberList = []
    leader = {}
    leader["dispName"] = request.json["dispName"]
    leader["level"] = "l"
    leader["location"] = []
    memberList.append(leader)
    doc["memberList"] = memberList
    result = groupClient.db[d["groupCode"]].insert_one(doc)
    #Return 200 & group code
    return jsonify(d), 200

def updateLoc(app, groupClient):
    if not request.json or not all(key in request.json for key in ("groupCode","dispName","loc")) or not len(request.json["loc"]) == 2:
        abort(400) # Bad request
    #Validate group code
    if (not (request.json["groupCode"].upper() in groupClient.db.collection_names())):
        abort(404)
    #Update member location
    group = groupClient.db[request.json["groupCode"].upper()].find()
    if group.count() > 1: #too many listings or none (should not be encountered)
        abort(400)
    doc = group.next()
    #Validate member
    if not request.json["dispName"] in doc["memberList"]:
        abort(404)
    #Update location for user
    for item in doc["memberList"]:
        if item["dispName"] == request.json["dispName"]:
            item["loc"] = request.json["loc"]
    #Update document
    result = groupClient.db[request.json["groupCode"].upper()].replace_one({"groupName": doc["groupName"]},doc)
    #Return 200
    return 200

def groupUpdate(app, groupClient, groupCode):
    d = {}
    d["lostList"] = []
    d["status"] = ""
    #Validate group code
    if (not (groupCode in groupClient.db.collection_names())):
        abort(404)
    #Check currently stored distance of members in group
    group = groupClient.db[request.json["groupCode"].upper()].find()
    if group.count() > 1: #too many listings or none (should not be encountered)
        abort(400)
    #Get leader coords & member coords
    leaderLoc = []
    memberLoc = []
    doc = group.next()
    triggerDist = doc["triggerDist"]
    origList = doc["memberList"]
    for item in origList:
        if item["level"] == "m":
            memberLoc.append(item)
        else:
            leaderLoc = item["location"]

    #Validate mem/leader
    for mem in memberLoc:
        if dist(leaderLoc, mem["location"]) > triggerDist:
            d["lostList"].append(mem)

    #Return 200 & status for members
    if len(d["lostList"]) == 0:
        d["status"] = "all clear"
    else:
        d["status"] == str(len(d["lostList"])) + " are lost"

    return 200, jsonify(d)

def groupEnd(app, groupClient, groupCode):
    #Validate group code
    if (not (groupCode in groupClient.db.collection_names())):
        abort(404)
    #Remove collection
    result = groupClient.db[groupCode].drop()
    #Return 200
    return 200

def dist(a,b):
    return math.sqrt((a[0]-b[0])^2 + (a[1]-b[1])^2)
