from flask import Flask
#from db import Connection

from uuid import uuid1
from flask import request

from endpoints.pool import Pool_heating_on
#from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId
import json


app=Flask(__name__)
## db=Connection('flask_mongo_crud')

## users = db.user.find({})


@app.get("/pool_on")
def get_users():
    return Pool_heating_on()


if __name__=="__main__":
    app.run(port=8887, debug=True)