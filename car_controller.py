import socket
import RPi.GPIO as GPIO

import globals
# Function For testing the pins to move all wheels in the forward direction
def ON():
    # RUN
    GPIO.output(globals.in1, GPIO.LOW)
    GPIO.output(globals.in2, GPIO.HIGH)
    p.ChangeDutyCycle(100)
    GPIO.output(globals.in3, GPIO.LOW)
    GPIO.output(globals.in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100)

# function to putting low voltage on all pins in1 in2 in3 in4
# and changing the duty cycle to 0 to stop the car
def Stop():
    # stop
    GPIO.output(globals.in1, GPIO.LOW)
    GPIO.output(globals.in2, GPIO.LOW)
    p.ChangeDutyCycle(0)
    GPIO.output(globals.in3, GPIO.LOW)
    GPIO.output(globals.in4, GPIO.LOW)
    p2.ChangeDutyCycle(0)


# Car Controller Functions
# Function to move car in the up right direction
# by making right wheels slower than left wheels
# p 75 duty cycle and p2 100 duty cycle multiplied by speed
def up_right():
    GPIO.output(globals.in1, GPIO.LOW)
    GPIO.output(globals.in2, GPIO.HIGH)
    p.ChangeDutyCycle(75 * globals.speed)
    GPIO.output(globals.in3, GPIO.LOW)
    GPIO.output(globals.in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100 * globals.speed)


# Function to move car in the up left direction
# by making left wheels slower than right wheels
# p2 75 duty cycle and p 100 duty cycle multiplied by speed
def up_left():
    GPIO.output(globals.in1, GPIO.LOW)
    GPIO.output(globals.in2, GPIO.HIGH)
    p.ChangeDutyCycle(100 * globals.speed)
    GPIO.output(globals.in3, GPIO.LOW)
    GPIO.output(globals.in4, GPIO.HIGH)
    p2.ChangeDutyCycle(75 * globals.speed)


# Function to move car in the down right direction
# by reversing direction with reversing pins in1 and in2
# and making right wheels slower than left wheels
# p 75 duty cycle and p2 100 duty cycle multiplied by speed
def down_right():
    GPIO.output(globals.in1, GPIO.HIGH)
    GPIO.output(globals.in2, GPIO.LOW)
    p.ChangeDutyCycle(75 * globals.speed)
    GPIO.output(globals.in3, GPIO.HIGH)
    GPIO.output(globals.in4, GPIO.LOW)
    p2.ChangeDutyCycle(100 * globals.speed)


# Function to move car in the down left direction
# by reversing direction with reversing pins in1 and in2
# and making left wheels slower than right wheels
# p2 75 duty cycle and p 100 duty cycle multiplied by speed
def down_left():
    GPIO.output(globals.in1, GPIO.HIGH)
    GPIO.output(globals.in2, GPIO.LOW)
    p.ChangeDutyCycle(100 * globals.speed)
    GPIO.output(globals.in3, GPIO.HIGH)
    GPIO.output(globals.in4, GPIO.LOW)
    p2.ChangeDutyCycle(75 * globals.speed)


# Function to move car in the forwarding direction
# by making all wheels move with the same amount of speed
# p2 100 duty cycle and p 100 duty cycle multiplied by speed
def up():
    GPIO.output(globals.in1, GPIO.LOW)
    GPIO.output(globals.in2, GPIO.HIGH)
    p.ChangeDutyCycle(100 * globals.speed)
    GPIO.output(globals.in3, GPIO.LOW)
    GPIO.output(globals.in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100 * globals.speed)


# Function to move car in the backward direction
# by reversing pins 1 and 2
# and making all wheels move with the same amount of speed
# p2 100 duty cycle and p 100 duty cycle multiplied by speed
def down():
    GPIO.output(globals.in1, GPIO.HIGH)
    GPIO.output(globals.in2, GPIO.LOW)
    p.ChangeDutyCycle(100 * globals.speed)
    GPIO.output(globals.in3, GPIO.HIGH)
    GPIO.output(globals.in4, GPIO.LOW)
    p2.ChangeDutyCycle(100 * globals.speed)


# Function to move car in the right direction
# by changing pins 1 and 2 and the opposite for 3 and 4
# and making only the left wheels move
# p2 100 duty cycle and p 0 duty cycle multiplied by speed
def right():
    GPIO.output(globals.in1, GPIO.LOW)
    GPIO.output(globals.in2, GPIO.HIGH)
    p.ChangeDutyCycle(0)
    GPIO.output(globals.in3, GPIO.LOW)
    GPIO.output(globals.in4, GPIO.HIGH)
    p2.ChangeDutyCycle(100 * globals.speed)


# Function to move car in the left direction
# by changing pins 1 and 2 and the opposite for 3 and 4
# and making only the right wheels move
# p 100 duty cycle and p2 0 duty cycle multiplied by speed
def left():
    GPIO.output(globals.in1, GPIO.LOW)
    GPIO.output(globals.in2, GPIO.HIGH)
    p.ChangeDutyCycle(100 * globals.speed)
    GPIO.output(globals.in3, GPIO.LOW)
    GPIO.output(globals.in4, GPIO.HIGH)
    p2.ChangeDutyCycle(0)


# Function to initialize the GPIO
# by setting the mode to GPIO.BCM
# and setting up the pins in1 in2 in3 in4
# and setting up the enable pins en1 and en2
# then putting the initial PWM signal
def GPIO_Init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(globals.in1, GPIO.OUT)
    GPIO.setup(globals.in2, GPIO.OUT)
    GPIO.setup(globals.en, GPIO.OUT)
    GPIO.setup(globals.in3, GPIO.OUT)
    GPIO.setup(globals.in4, GPIO.OUT)
    GPIO.setup(globals.en2, GPIO.OUT)
    GPIO.setup(globals.GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(globals.GPIO_ECHO, GPIO.IN)
    # PWM
    global p
    p = GPIO.PWM(globals.en, 100)
    global p2
    p2 = GPIO.PWM(globals.en2, 100)
    p.start(0)
    p2.start(0)

def car_Controller():
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 4445))
        sock.listen(1)
        print('Waiting for a Connection...')
        (client, (ip, sock)) = sock.accept()
        while True:
            try:
                print("Connected")
                data = client.recv(1024)
                print(data)
                if data == b'exit':
                    client.close()
                    break
                if data == b'':
                    # client.close()
                    continue
                if data == b'UDOWN':
                    print("up pressed")
                    globals.UP_Pressed = True
                elif data == b'DDOWN':
                    print("down pressed")
                    globals.Down_Pressed = True
                elif data == b'RDOWN':
                    print("right pressed")
                    globals.Right_Pressed = True
                elif data == b'LDOWN':
                    print("left pressed")
                    globals.Left_Pressed = True
                elif data == b'UUP':
                    globals.UP_Pressed = False
                    print("up released")
                elif data == b'DUP':
                    print("Down released")
                    globals.Down_Pressed = False
                elif data == b'RUP':
                    print("Right released")
                    globals.Right_Pressed = False
                elif data == b'LUP':
                    print("Left released")
                    globals.Left_Pressed = False

                if not data:
                    print("?")
                    # break
                # print ("Recieving Packet Number %d" %counter)
                # print(data)
                # counter += 1
            except:
                print("Error")
                # break

            try:
                print("the global stop",globals.stop)
                if globals.stop == False:
                    if globals.UP_Pressed and globals.Right_Pressed:
                        print("Right Forward")
                        up_right()
                    elif globals.UP_Pressed and globals.Left_Pressed:
                        print("left forward")
                        up_left()
                    elif globals.Down_Pressed and globals.Right_Pressed:
                        print("backward right")
                        down_right()
                    elif globals.Down_Pressed and globals.Left_Pressed:
                        print("backward Left")
                        down_left()
                    elif globals.UP_Pressed:
                        print("Move Forward")
                        up()
                    elif globals.Down_Pressed:
                        print("Move Backward")
                        down()
                    elif globals.Right_Pressed:
                        print("Move Right")
                        right()
                    elif globals.Left_Pressed:
                        print("Move Left")
                        left()
                    else:
                        print("Stop")
                        Stop()
            except Exception as e:
                print(e)
                print("break")
