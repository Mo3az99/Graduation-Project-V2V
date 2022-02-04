import socket
import time
import threading
# import io
import serial
import pynmea2
import serial
import os
import RPi.GPIO as GPIO
# buttons Variables
UP_Pressed = False
Down_Pressed = False
Right_Pressed = False
Left_Pressed = False
# input Definitions
in1 = 4
in2 = 3
en = 2
in3 = 22
in4 = 27
en2 = 23
def up_right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(75)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100)
def up_left():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(75)
def down_right():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(75)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(100)
def down_left():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(75)
def up():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100)
def down():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(100)
def right():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(0)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100)
def left():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    p.ChangeDutyCycle(100)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    p2.ChangeDutyCycle(0)
def GPIO_Init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.setup(en2, GPIO.OUT)
    # PWM
    global p
    p = GPIO.PWM(en, 100)
    global p2
    p2 = GPIO.PWM(en2, 100)
    p.start(0)
    p2.start(0)
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
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    p.ChangeDutyCycle(0)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(0)
# add Semaphore for Location
def current_location():
    # we dont need it global if it is only the command form the A9G
    global location
    global var_Location
    checkOK()
    time.sleep(1.1)
    location = ""
    # needs edit
    for i in range(0, 6):
        location = (ser.readline().decode('utf-8'))
    ser.write(b'AT+GPSRD=0\r')
    x = ser.read(1000)
    print(location)
    msg = pynmea2.parse(location)
    # improve convert msg.lat
    var_Location = (
            str(convert_lat(msg.lat)) + " °" + msg.lat_dir + "," + str(convert_long(msg.lon)) + " °" + msg.lon_dir)
    # print(msg.lon)
    print(getlocation_link(convert_lat(msg.lat), convert_long(msg.lon)))
def send():
    # location = getlocation()
    # sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    # nazlha ta7t 34an mkan el kolya et3ml update
    current_location()
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    send_socket.settimeout(0.2)
    message = str.encode("RPI Location " + var_Location)
    while True:
        send_socket.sendto(message, ('<broadcast>', 5037))
        print("message sent! \n")
        # Sleep for 1 second
        time.sleep(1)
def receive():
    PORT_NUMBER = 5037
    SIZE = 1024
    hostName = socket.gethostbyname('0.0.0.0')
    rev_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rev_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    rev_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rev_socket.bind((hostName, PORT_NUMBER))
    print("Test server listening on port {0}\n".format(PORT_NUMBER))
    while True:
        (data, addr) = rev_socket.recvfrom(SIZE)
        data1 = data.decode('utf-8')
        print(data1 + " From	" + str(addr) + "\n")
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
# def checkOKGPSON():
#     while 1:
#         rcv = ser.readline()
#         if rcv == b'+CME ERROR: 58\r\n':
#             ser.write(b'AT+GPS=1 \r')
#             print("Error Handled")
#         print(rcv)
#         if rcv == b'OK\r\n':
#             print("GPS ON")
#             break
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
def car_Controller():
    global UP_Pressed
    global Down_Pressed
    global Right_Pressed
    global Left_Pressed
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 4445))
        sock.listen(1)
        print('Waiting for a Connection...')
        (client, (ip, sock)) = sock.accept()
        counter = 1

        while True:
            try:
                data = client.recv(1024)
                print(data)
                if data == b'UDOWN':
                    print("up pressed")
                    UP_Pressed = True
                elif data == b'DDOWN':
                    print("down pressed")
                    Down_Pressed = True
                elif data == b'RDOWN':
                    print("right pressed")
                    Right_Pressed = True
                elif data == b'LDOWN':
                    print("left pressed")
                    Left_Pressed = True
                elif data == b'UUP':
                    UP_Pressed = False
                    print("up released")
                elif data == b'DUP':
                    print("Down released")
                    Down_Pressed = False
                elif data == b'RUP':
                    print("Right released")
                    Right_Pressed = False
                elif data == b'LUP':
                    print("Left released")
                    Left_Pressed = False

                if not data:
                    print("?")
                    break
                # print ("Recieving Packet Number %d" %counter)
                # print(data)
                # counter += 1
            except:
                print("???")
                break
            print("Connection Closed!")
            client.close()

            try:
                if UP_Pressed and Right_Pressed:
                    print("Right Forward")
                    up_right()
                elif UP_Pressed and Left_Pressed:
                    print("left forward")
                    up_left()
                elif Down_Pressed and Right_Pressed:
                    print("backward right")
                    down_right()
                elif Down_Pressed and Left_Pressed:
                    print("backward Left")
                    down_left()
                elif UP_Pressed:
                    print("Move Forward")
                    up()
                elif Down_Pressed:
                    print("Move Backward")
                    down()
                elif Right_Pressed:
                    print("Move Right")
                    right()
                elif Left_Pressed:
                    print("Move Left")
                    left()
                else:
                    print("Stop")
                    Stop()
            except Exception as e:
                print(e)
                print("break")


if __name__ == "__main__":
    # creating threads
    rev_thread = threading.Thread(target=receive)
    send_thread = threading.Thread(target=send)
    Car_thread = threading.Thread(target=car_Controller)

    # open Serial for COM 3 and baud rate 115200
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

    # initialize GPS
    init()
    # Initialize GPIO Pins and PWM
    GPIO_Init()
    # starting thread 1 for Receiving
    rev_thread.start()
    # starting thread 2 Main Thread
    send_thread.start()
    # starting thread 3 Car Thread
    Car_thread.start()
    time.sleep(60)
    exit()