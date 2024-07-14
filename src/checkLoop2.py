import glob

import os

from datetime import datetime

import time

from db import Connection

goalTemperature = 28

heating = False

import logging
logger = logging.getLogger(__name__)

logging.basicConfig(filename='pool.log', level=logging.INFO)
logger.info("Python Pool Temp Service is running")

#from endpoints.pool import Pool_heating_on, Pool_heating_off, Init_GPIO, Reset
db=Connection('pool_temp_test')

import RPi.GPIO as GPIO

in1 = 11
in2 = 13
in3 = 15

#Reset()

def Init_GPIO():

    logger.info("Initializing GPIO")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.output(in3, False)

def Pool_on():
    global heating
    if heating == False:
        # Set pool GPIO true
        logger.info("Turning pool on")
        GPIO.output(in3, True)
        heating = True
    else:
        logger.info("Heating is allready on")

def Pool_off():
    global heating
    if heating == True:
        # Set pool GPIO false
        logger.info("Turning pool off")
        GPIO.output(in3, False)
        heating = False
    else:
        logger.info("Heating is allready off")


def Get_temp():

    temperature = db.pool_temp
    result = temperature.find({}).sort("dateTime", -1).limit(1)
    return result[0]

def Get_config():

    config = db.pool_config
    result = config.find({}).limit(1)
    return result[0]

def Set_config():

    config = db.pool_config
    result = config.insert_one({"heating": True})
    print(result)

def Check_temp(config):
    # Get Temperature
    temp = Get_temp()["temp"]
    goal_temp = config["goal_temp"]
    logger.info("current temp:")
    logger.info(temp)
    logger.info("goal temp:")
    logger.info(goal_temp)

    delayHeating = config["delayHeating"]
    delayCooling = config["delayCooling"]

    print("Delay Heating:", delayHeating)
    print("Delay Cooling:", delayCooling)

    if (temp > goal_temp + delayHeating):
        logger.info("Turn off")
        Pool_off()
    elif (temp < goal_temp - delayCooling):
        logger.info("Turn on")
        Pool_on()
    elif ((temp > goal_temp - delayCooling) and (temp < goal_temp + delayHeating)): 
        logger.info("In the middle, just do nothing")

def Check_config(config):
    # Check Power State
    if config["heating"]:
        # Turn heating on
        Pool_on()
    else:
        # Turn heating off
        Pool_off()
        return
    Check_temp(config)

Init_GPIO()

while True:
    config = Get_config()
    #Set_config()
    logger.info("Checking for Changes")
    logger.info(config)
    Check_config(config)
    time.sleep(60)
