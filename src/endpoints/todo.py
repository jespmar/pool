from flask import Flask
from db import Connection

db=Connection('flask_mongo_crud')

from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId

def Insert_todo(content, user_id):

    content.update({"userId": ObjectId(user_id)})

    todos = db.todo
    result = todos.insert_one(content)
    print(result)

    content.update({"_id":str(result.inserted_id)})
    if not result.inserted_id:
        return {"message":"Failed to insert"}, 500

    return dumps(content, json_options=RELAXED_JSON_OPTIONS), {"Content-Type": "application/json"}

def Get_todos(user_id):
    query={
        "userId":ObjectId(user_id)
    }

    todos = db.todo.find(query)
    return dumps(list(todos), json_options=RELAXED_JSON_OPTIONS), {"Content-Type": "application/json"}

def Get_todo(todo_id):
    query={
        "_id":ObjectId(todo_id)
    }
    todo=db.todo.find_one(query)

    if not todo:
        return {
            "message":"User is not found"
        }, 404

    return dumps(todo, json_options=RELAXED_JSON_OPTIONS), {"Content-Type": "application/json"}

def Update_todo(todo_id, content):
    query={
        "_id":ObjectId(todo_id)
    }
    result=db.todo.update_one(query, content)

    if not result.matched_count:
        return {
            "message":"Failed to update. Record is not found"
        }, 404
    
    if not result.modified_count:
        return {
            "message":"No changes applied"
        }, 500
    
    return {"message":"Update success"}, 200

def Delete_todo(todo_id):
    query={
        "_id":ObjectId(todo_id)
    }
    result=db.todo.delete_one(query)
    
    if not result.deleted_count:
        return {
            "message":"Failed to delete"
        }, 500
    
    return {"message":"Delete success"}, 200