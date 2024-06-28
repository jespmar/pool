from flask import Flask

import glob

from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId


from datetime import datetime

import os

import time

import RPi.GPIO as GPIO

from checkLoop import logger

in1 = 11
in2 = 13
in3 = 15

Heating = False

def Init_GPIO():

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)

    GPIO.output(in1, False)
    GPIO.output(in2, False)
    GPIO.output(in3, False)


def Reset_state():
    global Heating
    f = open("../heating_state.txt", "r")
    state = f.read()
    if state == "on":
        Heating = True
        logger.info("Resetting state to ON")
        GPIO.output(in3, True)

def Write_state(state):
    f = open("../heating_state.txt", "w")
    f.write(state)

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
        Write_state("on")
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
        Write_state("off")
        GPIO.output(in1, False)
        GPIO.output(in3, False)
        power_on()
        return "Pool Heating OFF"
    else:
        logger.info("Heating is already OFF")
        return "Pool Heating already OFF"
    
    
