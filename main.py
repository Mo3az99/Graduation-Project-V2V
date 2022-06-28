import car_controller
import broadcast
import recieve
import ultrasonic
import threading
from globals import  logging ,  serial
import globals

def init():
    globals.ser.write(b'AT+GPS=1 \r')
    while 1:
        rcv = globals.ser.readline()
        if rcv == b'+CME ERROR: 58\r\n':
            globals.ser.write(b'AT+GPS=1 \r')
            print("Error Handled")
        #print(rcv)
        if rcv == b'OK\r\n':
            print("GPS ON")
            break


def receive_thread():
    recieve.receive()


def broadcast_thread():
    broadcast.broadcast()


def CarController_thread():
    car_controller.car_Controller()

def ultrasonic_thread():
    ultrasonic.ultrasonic()


if __name__ == "__main__":
    # creating threads
    rev_thread = threading.Thread(target=receive_thread)
    broadcast_thread = threading.Thread(target=broadcast_thread)
    Car_thread = threading.Thread(target=CarController_thread)
    Ultrasonic_thread = threading.Thread(target=ultrasonic_thread)
    # initialize GPS
    init()
    
    # Initialize GPIO Pins and PWM
    car_controller.GPIO_Init()
    # starting thread 1 for Receiving
    rev_thread.start()
    # starting thread 2 Main Thread
    broadcast_thread.start()
    # starting thread 3 Car Controlling Thread
    Car_thread.start()
    # starting thread 4 ultrasonic Calculating distance thread
    Ultrasonic_thread.start()
    #time.sleep(60)
    #exit()

