#24.738203, 46.684632 #follow
#24.742391052459563, 46.6823945413877 #lead
# 30.150110, 31.397541
from sympy import symbols, Eq, solve
from sympy import Symbol
# 30.134429, 31.389518

locationx = 30.134429
locationy = 31.389518
angle = 100
velocity= 80
acceleration = 0
DTCa =0
Following_vehicle = False
import math


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
    global Following_vehicle
    if(message.angle == angle):
        if(angle>0):
            if(message.locationx>locationx or message.locationy>locationy):
                print("ana following")
                Following_vehicle=True
            else:
                print("ana leading ")
        elif(angle<0):
            if (message.locationx < locationx or message.locationy < locationy):
                print("ana following to south ")
                Following_vehicle = True
            else:
                print("ana leading to south ")
    else:
        print("none of my business")
def determineDistanceToCollison(message):
    global acceleration
    global velocity
    global locationx
    global locationy
    global DTCa
    velocity = velocity * 0.27777777777778
    message.velocity = message.velocity * 0.27777777777778

    #v_Relative = abs(v_Relative)
    v_Relative = message.velocity - velocity
    print("relative" , v_Relative)
    haversine= Haversine()
    location_a, location_b = (message.locationx , message.locationy), (locationx , locationy)
    #range = math.sqrt(math.pow((message.locationx - locationx), 2) + math.pow((message.locationy - locationy), 2))
    range = haversine.distance(location_a, location_b)
    range =range * 1000
    print("range is", range )
    #t = math.pow(v_Relative,2)
    # if leading vehicle acceleration not equal zero
    if message.acceleration != 0:
        sqrtv = math.sqrt(math.pow(v_Relative, 2) + 2 * abs(message.acceleration) * range)
        # print(sqrtv)
        DTCa = ((-v_Relative - sqrtv )/message.acceleration) * velocity
        print("DTCa",DTCa)
        print("TTC", DTCa / velocity)
    #if leading and following vehicles not equal zero
    if acceleration != 0 and message.acceleration != 0:
        Dw1 =0.5 * ((pow(velocity,2)/acceleration) -(pow(message.velocity,2)/abs(message.acceleration))) + 1.5 * velocity + 1
        print("DW1",Dw1)
        Dw2 = ((pow(velocity,2)) /( 19.6 *( (acceleration/9.8) + 0.7)))+ 1.5 * velocity + 1
        print("DW2",Dw2)
        #D3
        Dw3 = (velocity * 1.5) - (0.5 * message.acceleration * pow(1.5, 2) )+1
        print("DW3",Dw3)
        #delta 1
        deltaD1 = DTCa-Dw1
        #delta 2
        deltaD2 = DTCa-Dw2
        #Delta 3
        deltaD3 = DTCa-Dw3
        #tw1
        tw1 = deltaD1 /velocity
        tw2 = deltaD2 / velocity
        tw3 = deltaD3 / velocity
        print("TW1",tw1)
        print("TW2", tw2)
        print("TW3", tw3)
        print("TTC",DTCa/velocity)
        if tw3 < 2:
            print("brake")
        elif tw2 < 2 :
            print("Danger")
        elif tw1 < 2 :
            print("warning ")
    elif message.acceleration == 0 and acceleration == 0:
        x = Symbol('x')

        s = (solve((acceleration * x ** 2) - (message.acceleration * x ** 2) + velocity * x - message.velocity * x - (range), x))
        print("TTC",s[0])
        if s[0] < 3 :
            print("Brake")
        elif s[0] < 5 :
            print("Danger")
        elif s[0] < 7 :
            print("warning")

    # print("Dw1",Dw1)
    # relative_acc = message.acceleration - acceleration
    # new_DTC = (math.pow(message.velocity ,2) / 2*message.acceleration) - (math.pow((message.velocity-v_Relative),2)/ 2*(message.acceleration-relative_acc)) + 2
    # DTCa = abs(DTCa)
    # TTC = DTCa/velocity
    # print("TTC", TTC )
    # print("DTCa" , DTCa)
    # print(DTCa)
    # return DTCa

    #Dw1 = 0.5((velocity**2 / acceleration) - ())


if __name__ == "__main__":
    # 30.150530, 31.398014
    # 30.150110, 31.397541
    # 30.135607, 31.391417
    # 30.136336, 31.392456
    variable = message(0, 30.136336, 31.392456, 60, 0 , 0, 100)
    determineLeadingVehicle(variable)
    if(Following_vehicle):
        determineDistanceToCollison(variable)


