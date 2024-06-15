from flask import Flask

import glob

from bson import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS
from bson.objectid import ObjectId

import os

import time

import RPi.GPIO as GPIO

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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
    time.sleep(160)
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
        return "Pool Heating ON"
    else:
        print("Heating already ON")
        return "Pool Heating already On"
    
def Pool_heating_off():
    global Heating
    if Heating == True:
        Heating = False
        print("pool heating off")
        GPIO.output(in1, False)
        GPIO.output(in3, False)
        power_on()
        return "Pool Heating OFF"
    else:
        print("Heating is already OFF")
        return "Pool Heating already OFF"
    
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
        return {"temp" : temp_c}
    
