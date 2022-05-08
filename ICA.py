import enum
import math
import numpy as np
#import matplotlib.pyplot as plt

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

def get_line_equation(P, Q):
    a = Q[1] - P[1]
    b = Q[0] - P[0]
    m = a/b
    print("slope",m)
    c = P[1] - m * P[0]
    print("b",c)
    print("y = ", m ,"x +" , c)


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
