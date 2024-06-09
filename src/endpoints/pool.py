from flask import Flask


from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId

import time

import RPi.GPIO as GPIO

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

def power_on():
    print("turning power on")
    GPIO.output(in2, True)
    time.sleep(15)
    print("turning power off")
    GPIO.output(in2, False)

def Pool_heating_on():
    global Heating
    if Heating == False:
        Heating = True
        print("Pool heating on")
        GPIO.output(in1, True)
        GPIO.output(in3, True)
        power_on()
        return "Pool Heating On"
    else:
        print("Heating already ON")
        return "Pool Heating already On"
    
