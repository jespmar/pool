from flask import Flask

import glob


from db import Connection

from datetime import datetime

import os

import time

import RPi.GPIO as GPIO

import logging
logger = logging.getLogger(__name__)


in1 = 11
in2 = 13
in3 = 15

Heating = False

db=Connection('pool_temp_test')


def Init_GPIO():

    logger.info("Initializing GPIO")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)

    GPIO.output(in1, False)
    GPIO.output(in2, False)
    GPIO.output(in3, False)


def Reset():
    logger.info("Resetting to prevent damage")
    GPIO.output(in1, False)
    GPIO.output(in3, False)
    power_on()
    logger.info("Reset Complete")

def Insert_state(state):

    State = db.state
    result = State.insert_one(state)
    print(result)

    state.update({"_id":str(result.inserted_id)})
    if not result.inserted_id:
        return {"message":"Failed to insert"}, 500

    return dumps(state, json_options=RELAXED_JSON_OPTIONS), {"Content-Type": "application/json"}

    

def Write_state(state):
    f = open("../heating_state.txt", "w")
    s = {"state": state, "dateTime": datetime.now()}
    f.write(state)
    Insert_state(s)

def power_on():
    print("turning power on")
    GPIO.output(in2, True)
    time.sleep(180)
    logger.info("turning power off")
    GPIO.output(in2, False)

def Pool_heating_on():
    global Heating
    if Heating == False:
        Heating = True
        logger.info("Pool heating on")
        GPIO.output(in1, True)
        GPIO.output(in3, True)
        power_on()
        return "Pool Heating ON"
    else:
        logger.info("Heating already ON")
        return "Pool Heating already On"
    
def Pool_heating_off():
    global Heating
    if Heating == True:
        Heating = False
        logger.info("pool heating off")
        GPIO.output(in1, False)
        GPIO.output(in3, False)
        power_on()
        return "Pool Heating OFF"
    else:
        logger.info("Heating is already OFF")
        return "Pool Heating already OFF"
    
    
