import uuid
import logging
import serial
import math
import numpy as np
import json
import time

#function to handel the logger
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger



# global variables
# message contant
vecid = uuid.getnode()
locationx = 0     #long
locationy = 0     #lat
point1 = []
point2 = []
line1 = []
stop = False
angle = 0
velocityx = 0
velocityy=0
direction = "STOPPED"
acceleration = 0
#previous location variables
prev_velocity =0
prev_locationx = 0
prev_locationy = 0
prev_velocityx =0
prev_velocityy = 0
#car current conditions
timee = 0
velocity =0
DTCa = 0
Following_vehicle = True
# Location and speed Global Variables
location = ""
speed = 0.5
# buttons Variables
UP_Pressed = False
Down_Pressed = False
Right_Pressed = False
Left_Pressed = False
# input Definitions
in1 = 4
in2 = 3
en = 2
in3 = 22
in4 = 27
en2 = 23
# set GPIO Pins for ultrasonic
GPIO_TRIGGER = 6
GPIO_ECHO = 5
# Port and size Variables
PORT_NUMBER = 5037
SIZE = 1024
#formatter for loggers
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# first file logger
logger = setup_logger('first_logger', 'first_logfile.log')
# second file logger
super_logger = setup_logger('second_logger', 'second_logfile.log')
super_logger.info(" Locations before kalman")
# Now we are going to Set the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
# open Serial for COM 3 and baud rate 115200
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)


