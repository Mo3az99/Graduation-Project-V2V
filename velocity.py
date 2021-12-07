from math import sin, cos, sqrt, atan2, radians
import time

class timeType:
    seconds =44


def convert_long(x):
    degree =float(str(x)[:3])
    minutes =float(str(x)[3:])
    result = degree+(minutes/60)
    return result

def convert_lat(x):
    degree =float(str(x)[:2])
    minutes =float(str(x)[2:])
    result = degree+(minutes/60)
    return result


def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
    R = 6371 # Radius of the earth in km
    dLat = radians(lat2-lat1)
    dLon = radians(lon2-lon1)
    rLat1 = radians(lat1)
    rLat2 = radians(lat2)
    a = sin(dLat/2) * sin(dLat/2) + cos(rLat1) * cos(rLat2) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c # Distance in km
    return d

def calc_velocity(dist_km, time_start, time_end):
    """Return 0 if time_start == time_end, avoid dividing by 0"""
    return dist_km / (time_end - time_start) if time_end > time_start else 0


if __name__ == "__main__":
    latitude1 =  54.9041349
    longitude1 = 11.8737433



    latitude2 =54.9088633
    longitude2 = 11.8681116

    time_start = 20


    time_end  = 60

    dest = getDistanceFromLatLonInKm(latitude1, longitude1, latitude2, longitude2)
    velo = calc_velocity(dest, time_start, time_end)

    print(dest)
    print(velo)


