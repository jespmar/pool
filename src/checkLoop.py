import glob

import os

from datetime import datetime

import time

from db import Connection

goalTemperature = 28

import logging
logger = logging.getLogger(__name__)

logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.info("Python Pool Temp Service is running")

#from endpoints.pool import Pool_heating_on, Pool_heating_off, Init_GPIO, read_temp, Write_state, Reset_state
db=Connection('pool_temp_test')

#Init_GPIO()
#Reset_state()

def Get_temp():

    temperature = db.pool_temp
    result = temperature.find({}).sort("dateTime", -1).limit(1)
    return result[0]


while True:
    logger.info("Checking for Changes")
    # Get Pool temp from Database
    #temp = Get_temp()
    #pool_temp = temp["temp"]
    #logger.info("Current Temp")
    #logger.info(pool_temp)
    #if pool_temp < goalTemperature - 1:
        # Check current state
        #Pool_heating_on()
        #Write_state("on")
        #print("on")
    #if pool_temp > goalTemperature + 0.5:
        # Check current state
        #Pool_heating_off()
        #Write_state("off")
        #print("off")
    time.sleep(30)