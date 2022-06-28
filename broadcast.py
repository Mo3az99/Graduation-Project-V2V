import socket
import pynmea2
import globals
import Kalman
from globals import json , time , serial , math
import FCA

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
    point1=[]
    point2=[]

    def __init__(self, vecid, locationx, locationy, velocityx, velocityy, acceleration, stop, angle, direction,point1,point2,line1):
        self.vecid = vecid
        self.locationx = locationx
        self.locationy = locationy
        self.velocityx = velocityx
        self.velocityy = velocityy
        self.acceleration = acceleration
        self.stop = stop
        self.angle = angle
        self.direction = direction
        self.point1 = point1
        self.point2 = point2
        self.line1 = line1

#Function to update speed
def checkOK():
    globals.ser.write(b'AT+GPSRD=1\r')
    while 1:
        rcv = globals.ser.readline()
        if rcv == b'+CME ERROR: 58\r':
            globals.ser.write(b'AT+GPSRD=1\r')
            print("Error Handled")
        print(rcv)
        if rcv == b'OK\r\n':
            print("GPSRD ON")
            break

def update_speed():

    if globals.prev_locationx == 0 and globals.prev_locationy == 0:
        globals.velocityx =  0
        globals.velocityy =  0
    else:
        globals.velocityx =abs(globals.locationx - globals.prev_locationx)
        globals.velocityy = abs(globals.locationy- globals.prev_locationy)

def update_angle():
    locationx_t=f'{globals.locationx:.5f}'[:-1]
    locationx_t = float(locationx_t)
    locationy_t=f'{globals.locationy:.5f}'[:-1]
    locationy_t = float(locationy_t)
    prev_locationx_t=f'{globals.prev_locationx:.5f}'[:-1]
    prev_locationx_t = float(prev_locationx_t)
    prev_locationy_t=f'{globals.prev_locationy:.5f}'[:-1]
    prev_locationy_t = float(prev_locationy_t)

    dLon = locationx_t - prev_locationx_t

    y = math.sin(dLon) * math.cos(locationy_t)
    x = math.cos(prev_locationy_t) * math.sin(locationy_t) - math.sin(prev_locationy_t) * math.cos(locationy_t) * math.cos(dLon)

    brng = math.atan2(y, x)

    brng = brng * (180.0 / 3.141592653589793238463)
    brng = (brng + 360)
    brng = brng % 360
    brng = 360 - brng

    globals.angle= brng
    #print(angle)

def update_acceleration():
    #globals.velocity = math.sqrt(math.pow(globals.velocityx, 2) + math.pow(globals.velocityy, 2))
    #globals.prev_velocity = math.sqrt(math.pow(globals.prev_velocityx, 2) + math.pow(globals.prev_velocityy, 2))
    globals.acceleration = abs(globals.velocity - globals.prev_velocity) /2
    print("ACCELERATION !!! ", globals.acceleration)
    

# 

# 
# add Semaphore for Location

# Function To get the current location of the moving vehicle
# and update the global variable Location
# and converting the format of GNRMC to latitude and longitude
# and setting up the Google maps link
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
def current_location():
    # we dont need it global if it is only the command form the A9G
    globals.prev_locationx = globals.locationx
    globals.prev_locationy = globals.locationy
    #globals.ser.flushInput()
    x = globals.ser.read(1000)

    checkOK()
    #print("1")
    # time.sleep(1.1)
    # needs edit
    while(1):
        temp_read = (globals.ser.readline().decode('utf-8'))
        #print("the line is ", temp_read)
        if temp_read[0:6] == "$GNRMC":
            globals.location = temp_read
            break
    #print("2")
    x = globals.ser.read(10000)
    print("empty  buffer")
    globals.ser.write(b'AT+GPSRD=0\r\n')
    while(1):
        rcv = globals.ser.readline()
        print(rcv)
        if rcv == b'OK\r\n':
            print("GPSRD OFF")
            break
    #globals.ser.flushInput()
    #globals.ser.flushOutput()
    
    
#     print("3")
    if globals.location != "":
        print(globals.location)
        msg = pynmea2.parse(globals.location)
        globals.locationx=convert_long(msg.lon)
        globals.locationy=convert_lat(msg.lat)
        globals.timee=msg.timestamp
        # print("Timestamp",globals.timee)
        globals.super_logger.info(globals.locationx)
        globals.super_logger.info(globals.locationy)
        # logger.info("Timestamp")
        # logger.info(timee)
        # var_Location = (
        #         str(convert_lat(msg.lat)) + " °" + msg.lat_dir + "," + str(convert_long(msg.lon)) + " °" + msg.lon_dir)
        print(getlocation_link(convert_lat(msg.lat), convert_long(msg.lon)))

def convertLatlonToXY(lat1,lon1,lat2,lon2):
    dx = (lon1 - lon2) * 40000 * math.cos((lat1 + lat2) * math.pi / 360) / 360
    # if negative to east
    # print("dx",dx)
    dy = (lat1 - lat2) * 40000 / 360
    # if negative to north
    # print("dy",dy)
    return dx, dy

def convertMeters(lat1, lon1, lat2, lon2):
    dx, dy = convertLatlonToXY(lat1, lon1, lat2, lon2)
    dx *= 1000
    dy *= 1000
    return dx , dy

# Function to get the Current Location from current_Location function and update the Global Location Variable
# preparing the socket for broadcasting and reusing the port
# finally we broadcast the location over the network and printing an Acknowledgement message
def broadcast():
    # location = getlocation()
    # sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    # nazlha ta7t 34an mkan el kolya et3ml update
    # current_location()
    print("ssssssssssssssssssssssssssssssssssssssssssssssssssssss")
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    send_socket.settimeout(0.2)
    current_location()
    #update_speed()
    update_angle()
    #update_acceleration()
    bcn1 = Kalman.bcnSample(globals.vecid, 0, globals.locationx, globals.locationy, globals.velocityx,globals.velocityy)
    klm = Kalman.kalmanTrack(bcn1, 0)
    while True:
        current_location()
        klm.predict()
        bcn1 = Kalman.bcnSample(globals.vecid, 0, globals.locationx, globals.locationy, globals.velocityx, globals.velocityy)
        klm.update(bcn1, 1)
        globals.locationx = klm.X[0]
        globals.locationy = klm.X[3]
        x1_car1, y1_car1 = convertMeters(globals.prev_locationy, globals.prev_locationx, 0, 0)
        globals.point1 = [x1_car1, y1_car1]
        x2_car1, y2_car1 = convertMeters(globals.locationy, globals.locationx, 0, 0)
        globals.point2 = [x2_car1, y2_car1]
        globals.line1 = [globals.point1,globals.point2]
        #update_speed()
        globals.velocityx=klm.X[1]
        globals.velocityy=klm.X[4]
        update_angle()
        #keda ba3d kalman should be deleted after test
        
        FCA.DetermineDirection(globals.prev_locationy,globals.prev_locationx,globals.locationy,globals.locationx)
        update_acceleration()
        print("Direction before Broadcast",globals.direction)
        #add kalman
        #send kalman cooridantes
        #globals.acceleration = math.sqrt(math.pow(klm.X[2], 2) + math.pow(klm.X[5], 2))
#        variable = message(globals.vecid, klm.X[0], klm.X[3], klm.X[1], klm.X[4], globals.acceleration, globals.stop, globals.angle, globals.direction,globals.point1,globals.point2,globals.line1)
        variable = message(globals.vecid, klm.X[0], klm.X[3], klm.X[1], globals.velocity, globals.acceleration, globals.stop, globals.angle, globals.direction,globals.point1,globals.point2,globals.line1)

        # Map your object into dict
        data_as_dict = vars(variable)

        # Serialize your dict object
        data_string = json.dumps(data_as_dict)
        send_socket.sendto(data_string.encode(encoding="utf-8") , ('<broadcast>',5037))
        globals.logger.info(data_as_dict)
        #tayha fl logger deh
        # send_socket.sendto(message, ('<broadcast>', 5037))
        print("message sent! \n")
        # Sleep for 1 second
        time.sleep(1)

