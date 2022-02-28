# haygelna message
# n extract and get lat and long and angle
# determine if u r leading this vehicle or following or none by angle and ur position
# 30.148472, 31.389889

# 30.150110, 31.397541
# 30.150530, 31.398014
locationx =30.150530
locationy =31.398014
angle = 45


class message(object):
    vecid = 0
    locationx = 0
    locationy=0
    velocity = 0
    acceleration = 0
    stop = 0
    angle = 0

    def __init__(self, vecid, locationx,locationy, velocity, acceleration, stop, angle):
        self.vecid = vecid
        self.locationx = locationx
        self.locationy = locationy
        self.velocity = velocity
        self.acceleration = acceleration
        self.stop = stop
        self.angle = angle

def determineLeadingVehicle(message):
    global locationx
    global locationy
    if(message.angle == angle):
        if(angle>0):
            if(message.locationx>locationx or message.locationy>locationy):
                print("ana following")
            else:
                print("ana leading ")
        elif(angle<0):
            if (message.locationx < locationx or message.locationy < locationy):
                print("ana following to south ")
            else:
                print("ana leading to south ")
    else:
        print("none of my business")


if __name__ == "__main__":
    # 30.150530, 31.398014
    # 30.150110, 31.397541
    variable = message(0, 30.150110, 31.397541, 66, 5, 0, 45)
    determineLeadingVehicle(variable)