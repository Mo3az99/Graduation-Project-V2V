import json
import socket
import time
import threading
# import io
import pynmea2
import serial
import os
import RPi.GPIO as GPIO
from sympy import symbols, Eq, solve
from sympy import Symbol
import math
import uuid
import logging
import numpy as np


# Location, Angle, Velocity, Acceleration and Distance to collison global variables
vecid = uuid.getnode()
locationx = 0     #long
locationy = 0     #lat
prev_locationx = 0
prev_locationy = 0
angle = 0
direction = ""
velocity =0
timee = 0
prev_velocity =0
velocityx = 0
velocityy=0
prev_velocityx =0
prev_velocityy = 0
acceleration = 0
stop = False
DTCa = 0
Following_vehicle = True

# Location and speed Global Variables
location = ""
speed = 1
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


#############################################################
# Classes
#Kalman Classes
class bcnSample(object):
    def __init__(self, vehId, timestamp, px, py, vx, vy) -> None:
        super().__init__()
        # self.bEncrypt = bEncrypted
        self.vehId = vehId
        # self.psym = psym # id for car bet8yr
        self.timestamp = timestamp
        self.px = px
        self.vx = vx
        self.py = py
        self.vy = vy
        # self.angle

class kalmanTrack(object):
    p0 = 50
    q = 0.7
    rp = 5
    rv = 2
    bcnT = 1
    lastTrackId = 0
    bKalmanParamInitialized = False

    def zeroo(self):
        self.id = -1
        self.bActive = True
        self.lifeTime = 0
        self.lastUpdateTime = -1
        self.vehId = 0
        # self.pseudonym

        # somestuff should be here MatrixXd H, F, P, Q, S, R, K, Sinv;

        self.P = np.zeros((3, 3))
        self.P[0, 0] = self.p0

        self.F = np.identity(3)
        self.F[0, 1] = self.bcnT
        self.F[0, 2] = (self.bcnT * self.bcnT) / 2
        self.F[1, 2] = self.bcnT

        self.H = np.eye(2,M = 3)

        self.Q = np.zeros((3, 3))
        self.Q = np.array([[(self.bcnT ** 4) / 4, (self.bcnT ** 3) / 3, (self.bcnT ** 2) / 2],
                           [(self.bcnT ** 3) / 2, (self.bcnT ** 2), self.bcnT],
                           [(self.bcnT ** 2) / 2, self.bcnT, 1]])
        self.Q * self.q

        self.R = np.zeros((2, 2))
        self.R = np.array([[self.rp, 0],
                           [0, self.rv]])

        self.X = np.zeros(6)

        self.S = np.zeros((2, 2))
        #self.S = np.dot((np.dot(self.H, self.P)), (self.H.transpose())) + self.R
        self.S = np.dot(self.H, np.dot(self.P, self.H.transpose())) + self.R

        self.Sinv = np.zeros((2, 2))
        self.Sinv = np.linalg.inv(self.S)

        self.Sdev = np.linalg.det(self.S)

        self.K = np.zeros((3, 2))

    def __init__(self, bcn: bcnSample, tm) -> None:
        super().__init__()
        self.zeroo()
        self.lastUpdateTime = tm
        kalmanTrack.lastTrackId += 1
        self.id = kalmanTrack.lastTrackId
        self.vehId = bcn.vehId
        # self.pseudonym = bcn.
        self.lifeTime = 1
        self.X[0] = (bcn.px)
        self.X[1] = (bcn.vx)
        self.X[3] = (bcn.py)
        self.X[4] = (bcn.vx)

    def predict(self) -> None:
        tmpx = self.X[0:3]
        print("tempX",tmpx)
        # print("F elly hatdrb feha",self.F)
        temp = np.dot(self.F, tmpx)
        # temp=np.dot(tmpx,self.F)
        print("First temp",temp)

        self.X[0] = temp[0]
        self.X[1] = temp[1]
        self.X[2] = temp[2]

        tmpx = self.X[3:6]
        print("second tempX", tmpx)
        temp = np.dot(self.F, tmpx)
        # temp = np.dot(tmpx,self.F)
        print("Second temp",temp)
        self.X[3] = temp[0]
        self.X[4] = temp[1]
        self.X[5] = temp[2]

        #self.P = self.F * self.P * self.F.transpose() + self.Q
        # print("F",self.F)
        # print("P", self.P)
        # print("F.T", self.F.T)
        # print("Q", self.Q)
        # print("F.P",np.dot(self.F, self.P))
        # print("F.P.F.T",np.dot(np.dot(self.F, self.P), self.F.T))
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
        print("p",self.P)



    def update(self, z: bcnSample, tm) -> None:


        zVec = np.zeros((2, 1))
        self.vehId = z.vehId
        # self.pseudonym = z.psym
        self.lifeTime += 1
        self.bActive = True
        self.lastUpdateTime = tm

        x_prior = self.X
        p_prior = self.P

      #  self.S = np.dot((np.dot(self.H, p_prior)), (self.H.transpose())) + self.R
        self.S = self.R + np.dot(self.H, np.dot(p_prior, self.H.T))

        self.Sinv = np.linalg.inv(self.S)
        self.Sdet = np.linalg.det(self.S)

        self.K = np.dot((np.dot(p_prior, self.H.T)), self.Sinv)

        zVec = np.array([z.px, z.vx])

        temp = (x_prior[0:3]) + np.dot(self.K, zVec - np.dot(self.H, (x_prior[0:3])))

        self.X[0] = temp[0]
        self.X[1] = temp[1]
        self.X[2] = temp[2]

        zVec = np.array([z.py, z.vy])  # momkn deh 8alat

        temp = (x_prior[3:6]) + np.dot(self.K, zVec - np.dot(self.H, (x_prior[3:6])))

        self.X[3] = temp[0]
        self.X[4] = temp[1]
        self.X[5] = temp[2]

        ik = np.eye(len(self.K), M=len(self.K)) - np.dot(self.K, self.H)

        self.P = np.dot((np.dot(ik, p_prior)), ik.transpose()) + np.dot((np.dot(self.K, self.R)), self.K.transpose())

#Haversine Class
class Haversine(object):

    def __init__(self, radius=6371):
        """."""
        self.EARTH_RADIUS = radius

    @property
    def get_location_a(self) -> tuple:
        return self.LOCATION_ONE

    property

    def get_location_b(self) -> tuple:
        return self.LOCATION_TWO

    def distance(self, point_a: tuple, point_b: tuple) -> float:
        """Public api for haversine formula."""
        if not (isinstance(point_a, tuple) and isinstance(point_b, tuple)):
            raise TypeError(
                """Expect point_a and point_b to be <class "tuple">, {} and {} were given""".format(
                    type(point_a), type(point_b)
                )
            )
        self.LOCATION_ONE = point_b
        self.LOCATION_TWO = point_a
        return self._calculate_distance(self.LOCATION_ONE, self.LOCATION_TWO)

    def _calculate_distance(self, pointA, pointB):
        latA, lngA = (float(i) for i in pointA)
        latB, lngB = (float(i) for i in pointB)
        phiA = math.radians(latA)
        phiB = math.radians(latB)
        change_in_latitude = math.radians(latB - latA)
        change_in_longitude = math.radians(lngB - lngA)
        a = (
                math.sin(change_in_latitude / 2.0) ** 2
                + math.cos(phiA) * math.cos(phiB) * math.sin(change_in_longitude / 2.0) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = self.EARTH_RADIUS * c
        return distance


# Message Class
class message(object):
    vecid = 0
    locationx = 0
    locationy = 0
    velocityx = 0
    velocityy = 0
    acceleration = 0
    stop = 0
    angle = 0
    direction = ""

    def __init__(self, vecid, locationx, locationy, velocityx, velocityy, acceleration, stop, angle, direction):
        self.vecid = vecid
        self.locationx = locationx
        self.locationy = locationy
        self.velocityx = velocityx
        self.velocityy = velocityy
        self.acceleration = acceleration
        self.stop = stop
        self.angle = angle
        self.direction = direction



def determineLeadingVehicle(message):
    global locationx
    global locationy
    global Following_vehicle
    print("recieved angle",message["angle"])
    print("recieved Direction", message["direction"])
    print("My angle",angle)
    print("My Direction",direction)
    if message["direction"] == direction :
        if direction == "EAST" or direction == "NORTH" :
            if message["locationx"] > locationx or message["locationy"] > locationy:
                print("ana following")
                Following_vehicle = True
            else:
                print("ana leading ")
        elif direction == "WEST" or direction == "SOUTH" :
            if message["locationx"] < locationx or message["locationy"] < locationy:
                print("ana following to south ")
                Following_vehicle = True
            else:
                print("ana leading to south ")
        else:
            print("Mlna4 Da3wa Ya MO7eee")
    # if abs(message["angle"] - angle) <= 3:
    #     print("trying to deetermine the leading vehicle")
    #     if angle > 0:
    #         if message["locationx"] > locationx or message["locationy"] > locationy:
    #             print("ana following")
    #             Following_vehicle = True
    #         else :
    #             print("ana leading ")
    #     elif angle < 0:
    #         if message["locationx"] < locationx or message["locationy"] < locationy:
    #             print("ana following to south ")
    #             Following_vehicle = True
    #         else:
    #             print("ana leading to south ")
    # else:
    #     print("none of my business")


def determineDistanceToCollison(message):
    global acceleration
    global velocity
    global locationx
    global locationy
    global DTCa
    velocity = velocity * 0.27777777777778
    receivedvelocity =math.sqrt(math.pow(message["velocityx"] , 2) + math.pow(message["velocityy"] , 2))
    receivedvelocity = receivedvelocity * 0.27777777777778

    # v_Relative = abs(v_Relative)
    v_Relative = receivedvelocity - velocity
    print("relative", v_Relative)
    haversine = Haversine()
    location_a, location_b = (message["locationx"], message["locationy"]), (locationx, locationy)
    # range = math.sqrt(math.pow((message.locationx - locationx), 2) + math.pow((message.locationy - locationy), 2))
    range = haversine.distance(location_a, location_b)
    range = range * 1000
    print("range is", range)
    #logger.info("range is", range)
    # t = math.pow(v_Relative,2)
    # if leading vehicle acceleration not equal zero
    if message["acceleration"] != 0 and velocity != 0:
        sqrtv = math.sqrt(math.pow(v_Relative, 2) + 2 * abs(message["acceleration"]) * range)
        # print(sqrtv)
        DTCa = ((-v_Relative - sqrtv) / message["acceleration"]) * velocity
        print("DTCa", DTCa)
        print("TTC", DTCa / velocity)
    # if leading and following vehicles not equal zero
    if acceleration != 0 and message["acceleration"] != 0:
        Dw1 = 0.5 * ((pow(velocity, 2) / acceleration) - (
                    pow(receivedvelocity, 2) / abs(message["acceleration"]))) + 1.5 * velocity + 1
        print("DW1", Dw1)
        Dw2 = ((pow(velocity, 2)) / (19.6 * ((acceleration / 9.8) + 0.7))) + 1.5 * velocity + 1
        print("DW2", Dw2)
        # D3
        Dw3 = (velocity * 1.5) - (0.5 * message["acceleration"] * pow(1.5, 2)) + 1
        print("DW3", Dw3)
        # delta 1
        deltaD1 = DTCa - Dw1
        # delta 2
        deltaD2 = DTCa - Dw2
        # Delta 3
        deltaD3 = DTCa - Dw3
        # tw1
        tw1 = deltaD1 / velocity
        tw2 = deltaD2 / velocity
        tw3 = deltaD3 / velocity
        print("TW1", tw1)
        print("TW2", tw2)
        print("TW3", tw3)
        print("TTC", DTCa / velocity)
        if tw3 < 2:
            print("brake")
            Stop()
            logger.info("BRAKE")
        elif tw2 < 2:
            print("Danger")
            logger.info("Danger")
        elif tw1 < 2:
            print("warning ")
            logger.info("warning")
    elif message["acceleration"] == 0 and acceleration == 0:
        x = Symbol('x')
        print(solve(
            (acceleration * x ** 2) - (message["acceleration"] * x ** 2) + velocity * x - receivedvelocity * x - (range),
            x))
        s= [0]
        print(s)
        s = (solve(
            (acceleration * x ** 2) - (message["acceleration"] * x ** 2) + velocity * x - receivedvelocity * x - (range),
            x))
        if len(s) == 0:
            s = [0] 
        print("TTC", s)
        if s[0] < 3:
            print("Brake")
            Stop()
            logger.info("BRAKE with Time")
        elif s[0] < 5:
            print("Danger")
            logger.info("Time Danger")
        elif s[0] < 7:
            print("warning")
            logger.info("Time warning")
    else:
        print("md5lt444")



########################################################


# Car Controller Functions
# Function to move car in the up right direction
# by making right wheels slower than left wheels
# p 75 duty cycle and p2 100 duty cycle multiplied by speed
def up_right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(75 * speed)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100 * speed)


# Function to move car in the up left direction
# by making left wheels slower than right wheels
# p2 75 duty cycle and p 100 duty cycle multiplied by speed
def up_left():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(100 * speed)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(75 * speed)


# Function to move car in the down right direction
# by reversing direction with reversing pins in1 and in2
# and making right wheels slower than left wheels
# p 75 duty cycle and p2 100 duty cycle multiplied by speed
def down_right():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(75 * speed)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(100 * speed)


# Function to move car in the down left direction
# by reversing direction with reversing pins in1 and in2
# and making left wheels slower than right wheels
# p2 75 duty cycle and p 100 duty cycle multiplied by speed
def down_left():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(100 * speed)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(75 * speed)


# Function to move car in the forwarding direction
# by making all wheels move with the same amount of speed
# p2 100 duty cycle and p 100 duty cycle multiplied by speed
def up():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(100 * speed)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100 * speed)


# Function to move car in the backward direction
# by reversing pins 1 and 2
# and making all wheels move with the same amount of speed
# p2 100 duty cycle and p 100 duty cycle multiplied by speed
def down():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(100 * speed)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(100 * speed)


# Function to move car in the right direction
# by changing pins 1 and 2 and the opposite for 3 and 4
# and making only the left wheels move
# p2 100 duty cycle and p 0 duty cycle multiplied by speed
def right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(0)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100 * speed)


# Function to move car in the left direction
# by changing pins 1 and 2 and the opposite for 3 and 4
# and making only the right wheels move
# p 100 duty cycle and p2 0 duty cycle multiplied by speed
def left():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(100 * speed)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(0)


# Function to initialize the GPIO
# by setting the mode to GPIO.BCM
# and setting up the pins in1 in2 in3 in4
# and setting up the enable pins en1 and en2
# then putting the initial PWM signal
def GPIO_Init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.setup(en2, GPIO.OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    # PWM
    global p
    p = GPIO.PWM(en, 100)
    global p2
    p2 = GPIO.PWM(en2, 100)
    p.start(0)
    p2.start(0)
    
#Calculate Distance with Ultrasonic
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

# Function For testing the pins to move all wheels in the forward direction
def ON():
    # RUN
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100)

# function to putting low voltage on all pins in1 in2 in3 in4
# and changing the duty cycle to 0 to stop the car
def Stop():
    # stop
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(0)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(0)
    
#Function to update speed
def update_speed():
    global prev_locationy
    global prev_locationx
    global velocityy
    global velocityx
    if prev_locationx == 0 and prev_locationy == 0:
        velocityx =  0
        velocityy =  0
    else:
        velocityx =abs(locationx - prev_locationx)
        velocityy = abs(locationy- prev_locationy)

def update_angle():
    global locationx
    locationx_t=f'{locationx:.5f}'[:-1]
    locationx_t = float(locationx_t)
    global locationy
    locationy_t=f'{locationy:.5f}'[:-1]
    locationy_t = float(locationy_t)
    global prev_locationx
    prev_locationx_t=f'{prev_locationx:.5f}'[:-1]
    prev_locationx_t = float(prev_locationx_t)
    global prev_locationy
    prev_locationy_t=f'{prev_locationy:.5f}'[:-1]
    prev_locationy_t = float(prev_locationy_t)
    global angle

    dLon = locationx_t - prev_locationx_t

    y = math.sin(dLon) * math.cos(locationy_t)
    x = math.cos(prev_locationy_t) * math.sin(locationy_t) - math.sin(prev_locationy_t) * math.cos(locationy_t) * math.cos(dLon)

    brng = math.atan2(y, x)

    brng = brng * (180.0 / 3.141592653589793238463)
    brng = (brng + 360)
    brng = brng % 360
    brng = 360 - brng

    angle= brng
    #print(angle)

def update_acceleration():
    global velocityy
    global velocityx
    global prev_velocityx
    global prev_velocityy
    global acceleration
    global velocity
    global prev_velocity
    global angle

    velocity = math.sqrt(math.pow(velocityx , 2) + math.pow(velocityy , 2))
    prev_velocity = math.sqrt(math.pow(prev_velocityx , 2) + math.pow(prev_velocityy , 2))
    acceleration = abs(velocity - prev_velocity)

# add Semaphore for Location

# Function To get the current location of the moving vehicle
# and update the global variable Location
# and converting the format of GNRMC to latitude and longitude
# and setting up the Google maps link
def current_location():
    # we dont need it global if it is only the command form the A9G
    global location
    global vecid
    global locationx
    global locationy
    global prev_locationx
    global prev_locationy
    global timee
    prev_locationx = locationx
    prev_locationy = locationy
    checkOK()
    # time.sleep(1.1)
    # needs edit
    for i in range(0, 8):
        temp_read = (ser.readline().decode('utf-8'))
        if temp_read[0:6] == "$GNRMC":
            location = temp_read
            break
    ser.write(b'AT+GPSRD=0\r')
    x = ser.read(1000)
    if location != "":
        print(location)
        msg = pynmea2.parse(location)
        locationx=convert_long(msg.lon)
        locationy=convert_lat(msg.lat)
        timee=msg.timestamp
        print("Timestamp",timee)
        super_logger.info(locationx )
        super_logger.info(locationy)
        # logger.info("Timestamp")
        # logger.info(timee)
        # var_Location = (
        #         str(convert_lat(msg.lat)) + " °" + msg.lat_dir + "," + str(convert_long(msg.lon)) + " °" + msg.lon_dir)
        print(getlocation_link(convert_lat(msg.lat), convert_long(msg.lon)))

# Function to get the Current Location from current_Location function and update the Global Location Variable
# preparing the socket for broadcasting and reusing the port
# finally we broadcast the location over the network and printing an Acknowledgement message
def broadcast():
    # location = getlocation()
    # sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    # nazlha ta7t 34an mkan el kolya et3ml update
    # current_location()
    global vecid
    global velocityy
    global velocityx
    global acceleration
    global angle
    global locationy
    global locationx
    global stop
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    send_socket.settimeout(0.2)
    current_location()
    update_speed()
    update_angle()
    update_acceleration()
    bcn1 = bcnSample(vecid, 0, locationx, locationy, velocityx,velocityy)
    klm = kalmanTrack(bcn1, 0)
    while True:
        current_location()
        klm.predict()
        bcn1 = bcnSample(vecid, 0, locationx, locationy, velocityx, velocityy)
        klm.update(bcn1, 1)
        locationx = klm.X[0]
        locationy = klm.X[3]

        update_speed()
        velocityx=klm.X[1]
        velocityy=klm.X[4]
        update_angle()
        #keda ba3d kalman should be deleted after test
        update_acceleration()
        #add kalman

        #send kalman cooridantes
        acceleration = math.sqrt(math.pow(klm.X[2], 2) + math.pow(klm.X[5], 2))
        variable = message(vecid, klm.X[0], klm.X[3], klm.X[1], klm.X[4], acceleration, stop, angle, direction)
        # Map your object into dict
        data_as_dict = vars(variable)

        # Serialize your dict object
        data_string = json.dumps(data_as_dict)
        send_socket.sendto(data_string.encode(encoding="utf-8") , ('<broadcast>',5037))
        logger.info(data_as_dict)
        # send_socket.sendto(message, ('<broadcast>', 5037))
        print("message sent! \n")
        # Sleep for 1 second
        time.sleep(1)

# Function to automatically reveive the location of the nearby vehicles
# by setting socket as DGRAM and reuse the socket for recieving the broadcasted message
# and Acknoledgeing with server is listening message
def receive():
    global PORT_NUMBER
    global SIZE
    hostName = socket.gethostbyname('0.0.0.0')
    rev_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rev_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    rev_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rev_socket.bind((hostName, PORT_NUMBER))
    print("Test server listening on port {0}\n".format(PORT_NUMBER))
    while True:
        data_encoded = rev_socket.recv(8192)
        data_string = data_encoded.decode(encoding="utf-8")
        data_variable = json.loads(data_string)
        # logger.info(data_variable)
        if data_variable["vecid"]==vecid:
           continue
        logger.info(data_variable)
        determineLeadingVehicle(data_variable)
        if Following_vehicle:
            print("Iam Following and going to check a possible FCA")
            determineDistanceToCollison(data_variable)

        # print(data_variable.locationx)
        # (data, addr) = rev_socket.recvfrom(SIZE)
        # data1 = data.decode('utf-8')
        # print(data1 + " From	" + str(addr) + "\n")

def init():
    ser.write(b'AT+GPS=1 \r')
    while 1:
        rcv = ser.readline()
        if rcv == b'+CME ERROR: 58\r\n':
            ser.write(b'AT+GPS=1 \r')
            print("Error Handled")
        print(rcv)
        if rcv == b'OK\r\n':
            print("GPS ON")
            break

def checkOK():
    ser.write(b'AT+GPSRD=1\r')
    while 1:
        rcv = ser.readline()
        if rcv == b'+CME ERROR: 58\r':
            ser.write(b'AT+GPSRD=1\r')
            print("Error Handled")
        print(rcv)
        if rcv == b'OK\r\n':
            print("GPSRD ON")
            break


# def checkOKGPSON():
#     while 1:
#         rcv = ser.readline()
#         if rcv == b'+CME ERROR: 58\r\n':
#             ser.write(b'AT+GPS=1 \r')
#             print("Error Handled")
#         print(rcv)
#         if rcv == b'OK\r\n':
#             print("GPS ON")
#             break
def convert_lat(x):
    degree = float(str(x)[:2])
    minutes = float(str(x)[2:])
    result = degree + (minutes / 60)
    return result


def getlocation_link(lat, lon):
    link = "http://maps.google.com/maps?q=loc:" + str(lat) + "," + str(lon)
    return link


def convert_long(x):
    degree = float(str(x)[:3])
    minutes = float(str(x)[3:])
    result = degree + (minutes / 60)
    return result

def convertLatlonToXY(lat1,lon1,lat2,lon2):
    dx = (lon1 - lon2) * 40000 * math.cos((lat1 + lat2) * math.pi / 360) / 360
    # if negative to east
    print(dx )
    dy = (lat1 - lat2) * 40000 / 360
    # if negative to north
    print(dy)
    return dx, dy

def calculateDistancinMeters(dx,dy):
    distance = math.sqrt(pow( dx, 2) + pow(dy, 2)) * 1000
    print("distance = ", distance, "meters")
    return distance

def DetermineDirection(lat1,lon1,lat2,lon2):
    global direction
    dx, dy = convertLatlonToXY(lat1, lon1, lat2, lon2)
    calculateDistancinMeters(dx,dy)
    dx*= -1000  # 2.5
    print("diffrence in x",dx)
    dy*= -1000  # 0.009
    print("diffrence in y",dy)
    if dx > 0  and (abs(dx)>2 or abs(dy)>2):
        if dy > 0 :
            if dx/dy >100:
                print("Heading East")
                direction = "EAST"
            elif dy/dx > 100:
                print("heading north")
                direction = "NORTH"
            else:
                print("Heading North East")
                direction = "NORTHEAST"
        if dy < 0:
            if dx/dy >100:
                print("Heading East")
                direction = "EAST"
            elif dy/dx > 100:
                print("heading south")
                direction = "SOUTH"
            else:
                print("Heading South East")
                direction = "SOUTHEAST"
    elif dx < 0 and (abs(dx)>2 or abs(dy >2)):
        if dy > 0 :
            if dx/dy >100:
                print("Heading West")
                direction = "WEST"
            elif dy/dx > 100:
                print("heading north")
                direction = "NORTH"
            else:
                print("Heading North West")
                direction = "NORTHWEST"
        if dy < 0:
            if dx/dy >100:
                print("Heading West")
                direction = "WEST"
            elif dy/dx > 100:
                print("heading south")
                direction = "SOUTH"
            else:
                print("Heading South West")
                direction = "SOUTHWEST"
    else:
        print("stopped")
        direction = "STOPPED"
    # slope = dy/dx
    # print("slope is ",slope)
    # a = [15, 12, 8, 8, 7, 7, 7, 6, 5, 3]
    # b = [10, 25, 17, 11, 13, 17, 20, 13, 9, 15]
    # print(linregress(a, b))
# Function to recieve commands from the controller android application
# and commanding the vehicle with the appropriate direction
# and handling any exception that could happen
def car_Controller():
    global UP_Pressed
    global Down_Pressed
    global Right_Pressed
    global Left_Pressed
    global stop
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 4445))
        sock.listen(1)
        print('Waiting for a Connection...')
        (client, (ip, sock)) = sock.accept()
        while True:
            try:
                print("Connected")
                data = client.recv(1024)
                print(data)
                if data == b'exit':
                    client.close()
                    break
                if data == b'':
                    # client.close()
                    continue
                if data == b'UDOWN':
                    print("up pressed")
                    UP_Pressed = True
                elif data == b'DDOWN':
                    print("down pressed")
                    Down_Pressed = True
                elif data == b'RDOWN':
                    print("right pressed")
                    Right_Pressed = True
                elif data == b'LDOWN':
                    print("left pressed")
                    Left_Pressed = True
                elif data == b'UUP':
                    UP_Pressed = False
                    print("up released")
                elif data == b'DUP':
                    print("Down released")
                    Down_Pressed = False
                elif data == b'RUP':
                    print("Right released")
                    Right_Pressed = False
                elif data == b'LUP':
                    print("Left released")
                    Left_Pressed = False

                if not data:
                    print("?")
                    # break
                # print ("Recieving Packet Number %d" %counter)
                # print(data)
                # counter += 1
            except:
                print("Error")
                # break

            try:
                if stop == False:
                    if UP_Pressed and Right_Pressed:
                        print("Right Forward")
                        up_right()
                    elif UP_Pressed and Left_Pressed:
                        print("left forward")
                        up_left()
                    elif Down_Pressed and Right_Pressed:
                        print("backward right")
                        down_right()
                    elif Down_Pressed and Left_Pressed:
                        print("backward Left")
                        down_left()
                    elif UP_Pressed:
                        print("Move Forward")
                        up()
                    elif Down_Pressed:
                        print("Move Backward")
                        down()
                    elif Right_Pressed:
                        print("Move Right")
                        right()
                    elif Left_Pressed:
                        print("Move Left")
                        left()
                    else:
                        print("Stop")
                        Stop()
            except Exception as e:
                print(e)
                print("break")
def ultrasonic():
    global stop
    try:
        while True:
            dist = distance()
            if dist < 50 :
                print("Warning")
                Stop()
                stop = True
            else :
                stop = False
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

if __name__ == "__main__":
    # creating threads
    rev_thread = threading.Thread(target=receive)
    broadcast_thread = threading.Thread(target=broadcast)
    Car_thread = threading.Thread(target=car_Controller)
    Ultrasonic_thread = threading.Thread(target=ultrasonic) 
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # first file logger
    logger = setup_logger('first_logger', 'first_logfile.log')
    # logger.info('This is just info message')

    # second file logger
    super_logger = setup_logger('second_logger', 'second_logfile.log')
    super_logger.info(" Locations before kalman")
    # super_logger.error('This is an error message')
    # logging.basicConfig(filename="carstop.log",
    #                     format='%(asctime)s %(message)s',
    #                     filemode='w')

    # Let us Create an object
    # logger = logging.getLogger()

    # Now we are going to Set the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)

    # open Serial for COM 3 and baud rate 115200
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

    # initialize GPS
    init()
    # Initialize GPIO Pins and PWM
    GPIO_Init()
    # starting thread 1 for Receiving
    rev_thread.start()
    # starting thread 2 Main Thread
    broadcast_thread.start()
    # starting thread 3 Car Controlling Thread
    Car_thread.start()
    # starting thread 4 ultrasonic Calculating distance thread
    Ultrasonic_thread.start()
    #time.sleep(60)
    #exit()

