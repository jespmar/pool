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

from endpoints.pool import Pool_heating_on, Pool_heating_off, Init_GPIO, Reset, Pool_mc_on
db=Connection('pool_temp_test')

Init_GPIO()

Pool_mc_on()
