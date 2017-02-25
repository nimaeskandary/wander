#!/usr/bin/env python3
# Morgan Wallace
# 2017

def joinGroup(app, groupClient, groupCode):
    if not request.json or not ("dispName" in request.json):
        abort(400) # Bad request
    #Validate group code in MONGO
    #Add member to group in MONGO
    #Return 200

def createGroup(app, groupClient):
    if not request.json or not all(key in request.json for key in ("groupName","dispName","triggerDist")):
        abort(400) # Bad request
    #


####EXAMPLE####
def save_practical(app, clients, PERNR, practical):
    if not request.json or not all(key in request.json for key in ("components","practical","status","name","PERNR","dateEdited")):
        abort(400) # Bad request
    d = {}
    d["agent"] = {}
    d["sup"] = {}
    now = datetime.datetime.now()
    request.json["dateEdited"] = now.strftime("%m/%d/%Y")
    # Add to agent database
    user = clients["agentclient"].db[request.json["PERNR"]].find()
    if user.count() == 0: # No documents for user
        # Create new agent
        p = {}
        p['prnrID'] = request.json["PERNR"]
        p['name'] = request.json["name"]
        result = clients["agentclient"].db[PERNR].insert_one(p)
    pracs = clients["agentclient"].db[PERNR].find({"practical": practical, "PERNR": request.json["PERNR"]}).count()
    if pracs == 0:
        result = clients["agentclient"].db[PERNR].insert_one(request.json)
        d["agent"][PERNR] = "all clear"
    elif pracs == 1:
        result = clients["agentclient"].db[PERNR].replace_one({"practical": practical},request.json)
        d["agent"][PERNR] = "all clear"
    else:
        d["agent"][PERNR] = "error adding %s practical" % practical # Too many practicals matching those results in DB (should never be hit unless specifically testing)
    # Add to sup database
    supsToUpdate = []
    for component in request.json['components']:
        if component["verified_by"] != "" and component["verified_by"] not in supsToUpdate:
            supsToUpdate.append(component["verified_by"])
    for sup in supsToUpdate:
        pracs = clients["supclient"].db[sup].find({"practical": practical, "PERNR": request.json["PERNR"]}).count()
        if pracs == 0:
            result = clients["supclient"].db[sup].insert_one(request.json)
            d["sup"][sup] = "all clear"
        elif pracs == 1:
            result = clients["supclient"].db[sup].replace_one({"practical": practical},request.json)
            d["sup"][sup] = "all clear"
        else:
            d["sup"][sup] = "error adding %s practical" % practical # Too many practicals matching those results in DB (should never be hit unless specifically testing)
    return jsonify(d), 200
