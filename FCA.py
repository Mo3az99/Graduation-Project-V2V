from sympy import symbols, Eq, solve
from sympy import Symbol
import globals
from globals import  math
import car_controller

class Haversine(object):

    def __init__(self, radius=6371):
        """."""
        self.EARTH_RADIUS = radius

    @property
    def get_location_a(self) -> tuple:
        return self.LOCATION_ONE

    @property

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
def convertLatlonToXY(lat1,lon1,lat2,lon2):
    dx = (lon1 - lon2) * 40000 * math.cos((lat1 + lat2) * math.pi / 360) / 360
    # if negative to east
    # print(dx)
    dy = (lat1 - lat2) * 40000 / 360
    # if negative to north
    # print(dy)
    return dx, dy

def calculateDistancinMeters(dx,dy):
    distance = math.sqrt(pow( dx, 2) + pow(dy, 2)) * 1000
    print("distance = ", distance, "meters")
    return distance

def DetermineDirection(lat1,lon1,lat2,lon2):
    dx, dy = convertLatlonToXY(lat1, lon1, lat2, lon2)
    globals.prev_velocity=globals.velocity
    globals.velocity=calculateDistancinMeters(dx,dy)
    dx*= -1000
    print("diffrence in x",dx)
    dy*= -1000
    print("diffrence in y",dy)
    if dx > 0  and (abs(dx)>1.8 or abs(dy >1.8)):
        if dy > 0 :
            if dx/dy >100:
                print("Heading East")
                globals.direction = "EAST"
            elif dy/dx > 100:
                print("heading north")
                globals.direction = "NORTH"
            else:
                print("Heading North East")
                globals.direction = "NORTHEAST"
        if dy < 0:
            if dx/dy >100:
                print("Heading East")
                globals.direction = "EAST"
            elif dy/dx > 100:
                print("heading south")
                globals.direction = "SOUTH"
            else:
                print("Heading South East")
                globals.direction = "SOUTHEAST"
    elif dx < 0 and (abs(dx)>1.5 or abs(dy >1.5)):
        if dy > 0 :
            if dx/dy >100:
                print("Heading West")
                globals.direction = "WEST"
            elif dy/dx > 100:
                print("heading north")
                globals.direction = "NORTH"
            else:
                print("Heading North West")
                globals.direction = "NORTHWEST"
        if dy < 0:
            if dx/dy >100:
                print("Heading West")
                globals.direction = "WEST"
            elif dy/dx > 100:
                print("heading south")
                globals.direction = "SOUTH"
            else:
                print("Heading South West")
                globals.direction = "SOUTHWEST"
    else:
        print("The car is stopped")
        globals.direction = "STOPPED"

def determineLeadingVehicle(message):

    #print("recieved angle",message["angle"])
    print("recieved Direction", message["direction"])
    #print("My angle",globals.angle)
    print("My Direction",globals.direction)
    if message["direction"] == globals.direction :
        print("Directions are the same")
        if globals.direction == "EAST" :
            if message["locationx"] > globals.locationx:
                print("ana following")
                globals.Following_vehicle = True
            else:
                print("ana leading ")
                globals.Following_vehicle = False
        elif globals.direction == "NORTH" :
            if message["locationy"] > globals.locationy:
                print("ana following")
                globals.Following_vehicle = True
            else:
                print("ana leading ")
                globals.Following_vehicle = False
        elif globals.direction == "NORTHEAST"
            if message["locationx"] > globals.locationx and message["locationy"] > globals.locationy:
                print("ana following")
                globals.Following_vehicle = True
            else:
                print("ana leading ")
                globals.Following_vehicle = False
        elif globals.direction == "WEST":
            if message["locationx"] < globals.locationx:
                print("ana following to west ")
                globals.Following_vehicle = True
            else:
                print("ana leading to west ")
                globals.Following_vehicle = False
                
        elif globals.direction == "SOUTH":
            if message["locationy"] < globals.locationy:
                print("ana following to south ")
                globals.Following_vehicle = True
            else:
                print("ana leading to south ")
                globals.Following_vehicle = False
        elif globals.direction ==  "SOUTWEST":
            if message["locationx"] < globals.locationx and message["locationy"] < globals.locationy:
                print("ana following to SOUTWEST ")
                globals.Following_vehicle = True
            else:
                print("ana leading to SOUTWEST ")
                globals.Following_vehicle = False
        elif globals.direction == "NORTHWEST" :
            if message["locationx"] < globals.locationx and message["locationy"] > globals.locationy:
                print("ana following to NORTHWEST ")
                globals.Following_vehicle = True
            else:
                print("ana leading to North west")
                globals.Following_vehicle = False
        elif globals.direction == "SOUTHEAST" :
            if message["locationx"] > globals.locationx and message["locationy"] < globals.locationy:
                print("ana following to SOUTHEAST ")
                globals.Following_vehicle = True
            else:
                print("ana leading to SOUTH EAST")
                globals.Following_vehicle = False
        else:
            print("Cars are not in the same Direction")
            globals.Following_vehicle = False
    else:
            print("car stopped so will not check FCA")
            globals.Following_vehicle = False
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

    #globals.velocity = globals.velocity * 0.27777777777778
    #receivedvelocity =math.sqrt(math.pow(message["velocityx"] , 2) + math.pow(message["velocityy"] , 2))
    #receivedvelocity = receivedvelocity * 0.27777777777778
    receivedvelocity = message["velocityy"]
    # v_Relative = abs(v_Relative)
    v_Relative = receivedvelocity - globals.velocity
    print("relative", v_Relative)
    haversine = Haversine()
    location_a, location_b = (message["locationx"], message["locationy"]), (globals.locationx, globals.locationy)
    # range = math.sqrt(math.pow((message.locationx - locationx), 2) + math.pow((message.locationy - locationy), 2))
    range = haversine.distance(location_a, location_b)
    range = range * 1000
    print("range is", range)
    #logger.info("range is", range)
    # t = math.pow(v_Relative,2)
    # if leading vehicle acceleration not equal zero
    if message["acceleration"] != 0 and globals.velocity != 0:
        sqrtv = math.sqrt(math.pow(v_Relative, 2) + 2 * abs(message["acceleration"]) * range)
        # print(sqrtv)
        globals.DTCa = ((-v_Relative - sqrtv) / message["acceleration"]) * globals.velocity
        print("DTCa", globals.DTCa)
        #print("TTC", globals.DTCa / globals.velocity)
    # if leading and following vehicles not equal zero
    print("1",globals.velocity,"2",globals.acceleration,"3",message["velocityy"],"4",message["acceleration"])
    if globals.acceleration != 0 and message["acceleration"] != 0:
        #it maybe changed to global
        Dw1 = 0.5 * ((pow(globals.velocity, 2) / globals.acceleration) - (
                    pow(receivedvelocity, 2) / abs(message["acceleration"]))) + 1.5 * globals.velocity + 1
        print("DW1", Dw1)
        Dw2 = ((pow(globals.velocity, 2)) / (19.6 * ((globals.acceleration / 9.8) + 0.7))) + 1.5 * globals.velocity + 1
        print("DW2", Dw2)
        # D3
        Dw3 = (globals.velocity * 1.5) - (0.5 * message["acceleration"] * pow(1.5, 2)) + 1
        print("DW3", Dw3)
        # delta 1
        deltaD1 = globals.DTCa - Dw1
        # delta 2
        deltaD2 = globals.DTCa - Dw2
        # Delta 3
        deltaD3 = globals.DTCa - Dw3
        # tw1
        #print(globals.velocity)
        tw1 = abs(deltaD1 / globals.velocity)
        tw2 = abs(deltaD2 / globals.velocity)
        tw3 = abs(deltaD3 / globals.velocity)
        print("TW1", tw1)
        print("TW2", tw2)
        print("TW3", tw3)
        ttc= abs(globals.DTCa / globals.velocity)
        print("TTC", ttc)
        if ttc < tw3 :
            print("brake")
            car_controller.Stop()
            globals.stop=True
            globals.logger.info("BRAKE")
        elif ttc < tw2 :
            print("Danger")
            globals.logger.info("Danger")
        elif ttc < tw1 :
            print("warning ")
            globals.logger.info("warning")
            globals.stop=False
        else:
            globals.stop=False
    # we should change it
    elif message["acceleration"] == 0 and globals.acceleration == 0:
        x = Symbol('x')
        print(solve(
            (globals.acceleration * x ** 2) - (message["acceleration"] * x ** 2) + globals.velocity * x - receivedvelocity * x - (range),
            x))
        s= [0]
        print(s)
        s = (solve(
            (globals.acceleration * x ** 2) - (message["acceleration"] * x ** 2) + globals.velocity * x - receivedvelocity * x - (range),
            x))
        if len(s) == 0:
            s = [0]
        print("TTC", s)
        if s[0] < 3:
            print("Brake")
            car_controller.Stop()
            globals.logger.info("BRAKE with Time")
        elif s[0] < 5:
            print("Danger")
            globals.logger.info("Time Danger")
        elif s[0] < 7:
            print("warning")
            globals.logger.info("Time warning")
    else:
        print("md5lt444 3aaa")

