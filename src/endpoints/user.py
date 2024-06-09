from flask import Flask
from db import Connection

db=Connection('flask_mongo_crud')

from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId

def Insert_user(content):

    users = db.user
    result = users.insert_one(content)
    print(result)

    content.update({"_id":str(result.inserted_id)})
    if not result.inserted_id:
        return {"message":"Failed to insert"}, 500


    return dumps(content, json_options=RELAXED_JSON_OPTIONS), {"Content-Type": "application/json"}

def Get_users():
    users = db.user.find({})
    return dumps(list(users), json_options=RELAXED_JSON_OPTIONS), {"Content-Type": "application/json"}

def Get_user(user_id):
    query={
        "_id":ObjectId(user_id)
    }
    user=db.user.find_one(query)

    if not user:
        return {
            "message":"User is not found"
        }, 404

    return dumps(user, json_options=RELAXED_JSON_OPTIONS), {"Content-Type": "application/json"}

def Update_user(user_id, content):
    query={
        "_id":ObjectId(user_id)
    }
    result=db.user.update_one(query, content)

    if not result.matched_count:
        return {
            "message":"Failed to update. Record is not found"
        }, 404
    
    if not result.modified_count:
        return {
            "message":"No changes applied"
        }, 500
    
    return {"message":"Update success"}, 200

def Delete_user(user_id):
    query={
        "_id":ObjectId(user_id)
    }
    result=db.user.delete_one(query)
    
    if not result.deleted_count:
        return {
            "message":"Failed to delete"
        }, 500
    
    return {"message":"Delete success"}, 200