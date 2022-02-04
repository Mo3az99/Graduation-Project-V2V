import xlwt
from xlwt import Workbook
import socket
import time
import threading
#import io
import pynmea2
import serial
import RPi.GPIO as GPIO
#from time import sleep
#input Definitions
in1 = 4
in2 = 3
en = 2
in3 = 22
in4 = 27
en2 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
p = GPIO.PWM(en, 50)
p2 = GPIO.PWM(en2, 50)
p.start(0)
p2.start(0)
    

#PWM
#GPIO_Init()


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

def current_location():
    # we dont need it global if it is only the command form the A9G
    global location
    global var_Location
    checkOK()

    time.sleep(1.1)
    location = ""
    #needs edit
    for i in range(0, 6):
        location = (ser.readline().decode('utf-8'))
    ser.write(b'AT+GPSRD=0\r')
    x=ser.read(1000)
    print(location)
    # print(x)
    msg = pynmea2.parse(location)

    # improve convert msg.lat
    #var_Location = (str(convert_lat(msg.lat)) +" °"+ msg.lat_dir +", "+str(convert_long(msg.lon)) + " °"+ msg.lon_dir )
    #print(str(convert_lat(msg.lat)))
    #return str(convert_lat(msg.lat))
    return msg
    #print(getlocation_link(convert_lat(msg.lat), convert_long(msg.lon)))
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

def ON():
    # RUN
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100)
def Stop():
    # stop
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    p.ChangeDutyCycle(0)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    p2.ChangeDutyCycle(0)



if __name__ == "__main__":
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    #open Serial for COM 3 and baud rate 115200
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    #initialize GPS
    init()
    ON()

    for i in range (0,10):
        message = current_location()
        sheet1.write(i, 0, str(convert_lat(message.lat)))
        sheet1.write(i, 1, str(convert_long(message.lon)))

    wb.save('xlwt example.xls')
    Stop()
    print("5lst<3")




