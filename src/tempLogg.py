import glob

import os

from datetime import datetime

import time

from db import Connection

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

db=Connection('pool_temp_test')


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return {"temp" : temp_c, "dateTime": datetime.now()}
    

def Insert_temp(content):

    temperature = db.pool_temp
    result = temperature.insert_one(content)
    print(result)

    content.update({"_id":str(result.inserted_id)})
    if not result.inserted_id:
        return {"message":"Failed to insert"}, 500

    return dumps(content, json_options=RELAXED_JSON_OPTIONS), {"Content-Type": "application/json"}


while True:
    temp = read_temp()
    Insert_temp(temp)
    print("Inserted temp")
    print(temp)
    time.sleep(600)