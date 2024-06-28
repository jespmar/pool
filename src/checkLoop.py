import glob

import os

from datetime import datetime

import time

from db import Connection

goalTemperature = 28

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId

from endpoints.pool import Pool_heating_on, Pool_heating_off, Init_GPIO, read_temp

db=Connection('pool_temp_test')

Init_GPIO()

def Get_temp():

    temperature = db.pool_temp
    result = temperature.find({}).sort("dateTime", -1).limit(1)
    return result[0]

while True:
    # Get Pool temp from Database
    temp = Get_temp()
    pool_temp = temp["temp"]
    if pool_temp < goalTemperature - 0.5:
        # Check current state
        Pool_heating_on()
    if pool_temp > goalTemperature + 0.5:
        # Check current state
        Pool_heating_off()
    time.sleep(600)