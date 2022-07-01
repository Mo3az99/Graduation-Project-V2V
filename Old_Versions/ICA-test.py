import enum
import math
import numpy as np
import matplotlib.pyplot as plt

direction = "Stopped"
direction1 = "Stopped"
direction2 = "Stopped"
ddx=0
ddy=0
gdx = 0
gdy =0
gd2x=0
gd2y=0
# creating enumerations using class
class Direction(enum.Enum):
    Stopped = 0
    North = 1
    North_East = 2
    East = 3
    South_East = 4
    South = 5
    South_West = 6
    West = 7
    North_West = 8




def determineDirectionNumber(directionstring ):
    if directionstring == "NORTH":
        direction = 1
    elif directionstring == "NORTHEAST":
        direction = 2
    elif directionstring == "EAST":
        direction = 3
    elif directionstring == "SOUTHEAST":
        direction = 4
    elif directionstring == "SOUTH":
        direction = 5
    elif directionstring == "SOUTHWEST":
        direction = 6
    elif directionstring == "WEST":
        direction = 7
    elif directionstring == "NORTHWEST":
        direction = 8
    else:
        direction = 0
    return direction

def calculateDistance(dx,dy):
    distance = math.sqrt(pow( dx, 2) + pow(dy, 2))
    print("distance = ", distance, "meters")
    return distance
def calculateDistancinMeters(dx,dy):
    distance = math.sqrt(pow( dx, 2) + pow(dy, 2)) * 1000
    print("distance = ", distance, "meters")
    return distance

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
def DetermineDirection(lat1,lon1,lat2,lon2):
    global direction
    global ddx
    global ddy
    dx, dy = convertLatlonToXY(lat1, lon1, lat2, lon2)
    calculateDistancinMeters(dx,dy)
    dx*= 1000  # 2.5
    ddx = dx
    print("diffrence in x",dx)
    dy*= 1000  # 0.009
    ddy = dy
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

# Car 1 South East
lat1 = 30.064035
lon1 = 31.280896

lat2 = 30.063818
lon2 = 31.280997

speedx = lon2 - lon1
speedy = lat2 - lat1
# Car 2 North East
lat11 = 30.062966
lon11 = 31.279479

lat22 = 30.063221
lon22 = 31.280222
speed2x = lon22 - lon11
speed2y = lat22 - lat11

#car 3
lat3=30.06114895172160
lon3=31.34806015302690
lat4=30.06116783806082
lon4=31.34799782470913

DetermineDirection(lat1,lon1,lat2,lon2)
gdx = ddx
gdy = ddy
direction1 = direction
direction1 = determineDirectionNumber(direction1)

DetermineDirection(lat11,lon11,lat22,lon22)
gd2x = ddx
gd2y = ddy
direction2 = direction
direction2 = determineDirectionNumber(direction2)
print("Car1",direction1)
print(Direction(direction1))
print("diffrence x",gdx)
print("diffrence y",gdy)
print("speed x",gdx/60,"M/s")
print("speed y",gdy/60,"M/S")

print("Car2",direction2)
print(Direction(direction2))
print("diffrence 2 x",gd2x)
print("diffrence 2 y",gd2y)
print("speed 2 x",gd2x/60 , "M/S")
print("speed 2 y",gd2y/60, "M/S")

DetermineDirection(lat4,lon4,lat3,lon3)
DetermineDirection(lat4,lon4,0,0)
DetermineDirection(lat3,lon3,0,0)
xx,yy= convertMeters(lat4,lon4,lat3,lon3)
print(xx,yy)
xx_prev,yy_prev= convertMeters(lat3,lon3,0,0)
print(xx_prev,yy_prev)
xx,yy= convertMeters(lat4,lon4,0,0)
print(xx,yy)
print(xx- xx_prev,yy-yy_prev)

location_x_1 = 3363945.0559780253
location_y_1 = 3340129.7597845355
location_x_2 = 3363951.893288374
location_y_2 = 3340127.6613024


def get_line_equation(P, Q):
    a = Q[1] - P[1]
    b = Q[0] - P[0]
    m = a/b
    print("slope",m)
    c = P[1] - m * P[0]
    print("b",c)
    print("y = ", m ,"x +" , c)

p = [3363945.0559780253,3340129.7597845355]
q = [3363951.893288374,3340127.6613024]
xx,yy= convertMeters(30.038562,31.299329,0,0)
point_test1 = [xx,yy]
xx,yy= convertMeters(30.038877,31.299656,0,0)
print("bsbsbs",xx,yy)
point_test2 = [xx,yy]

xx,yy= convertMeters(30.038624,31.300457,0,0)
point_test3 = [xx,yy]
xx,yy= convertMeters(30.039028,31.299998,0,0)
point_test4 = [xx,yy]

get_line_equation(p,q)
line1 = [point_test1,point_test2]
p2 = [3363445.0559780253,3344129.7597845355]
q2 = [3364451.893288374,3344427.6613024]
line2 = [point_test3,point_test4]

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
point_x,point_y =line_intersection(line1, line2)
print(point_x,point_y)
xx,yy = convertMeters(30.039130238048013, 31.299927008791443,0,0)
print(xx,yy)

# 3358957.3415458235 3337679.2445420963
# point_test2

dti= calculateDistance(xx - point_test2[0], yy - point_test2[1])
tti = dti / 2.5
print("tti", tti)
print("test Ended")

x1_car1,y1_car1= convertMeters(prev_locationy,prev_locationx,0,0)
point1 = [x1_car1,y1_car1]
x2_car1,y2_car1= convertMeters(locationy,locationx,0,0)
point2 = [x2_car1,y2_car1]

