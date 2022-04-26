
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

def determineLeadingVehicle(message):

    print("recieved angle",message["angle"])
    print("recieved Direction", message["direction"])
    print("My angle",globals.angle)
    print("My Direction",globals.direction)
    if message["direction"] == globals.direction :
        if globals.direction == "EAST" or globals.direction == "NORTH" :
            if message["locationx"] > globals.locationx or message["locationy"] > globals.locationy:
                print("ana following")
                Following_vehicle = True
            else:
                print("ana leading ")
        elif globals.direction == "WEST" or globals.direction == "SOUTH" :
            if message["locationx"] < globals.locationx or message["locationy"] < globals.locationy:
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

    globals.velocity = globals.velocity * 0.27777777777778
    receivedvelocity =math.sqrt(math.pow(message["velocityx"] , 2) + math.pow(message["velocityy"] , 2))
    receivedvelocity = receivedvelocity * 0.27777777777778
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
        globals.DTCa = ((-v_Relative - sqrtv) / message["acceleration"]) * globals.avelocity
        print("DTCa", globals.DTCa)
        print("TTC", globals.DTCa / globals.velocity)
    # if leading and following vehicles not equal zero
    if globals.acceleration != 0 and message["acceleration"] != 0:
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
        tw1 = deltaD1 / globals.velocity
        tw2 = deltaD2 / globals.velocity
        tw3 = deltaD3 / globals.velocity
        print("TW1", tw1)
        print("TW2", tw2)
        print("TW3", tw3)
        print("TTC", globals.DTCa / globals.velocity)
        if tw3 < 2:
            print("brake")
            car_controller.Stop()
            globals.logger.info("BRAKE")
        elif tw2 < 2:
            print("Danger")
            globals.logger.info("Danger")
        elif tw1 < 2:
            print("warning ")
            globals.logger.info("warning")
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
        print("md5lt444")

