# Message Class
import math
import socket
import pynmea2

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

