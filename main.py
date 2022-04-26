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
        print(rcv)
        if rcv == b'OK\r\n':
            print("GPS ON")
            break

if __name__ == "__main__":
    # creating threads
    rev_thread = threading.Thread(target=recieve.receive())
    broadcast_thread = threading.Thread(target=broadcast.broadcast())
    Car_thread = threading.Thread(target=car_controller.car_Controller())
    Ultrasonic_thread = threading.Thread(target=ultrasonic.ultrasonic())
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # first file logger
    globals.logger = globals.setup_logger('first_logger', 'first_logfile.log')
    # logger.info('This is just info message')

    # second file logger
    globals.super_logger = globals.setup_logger('second_logger', 'second_logfile.log')
    globals.super_logger.info(" Locations before kalman")
    # super_logger.error('This is an error message')
    # logging.basicConfig(filename="carstop.log",
    #                     format='%(asctime)s %(message)s',
    #                     filemode='w')

    # Let us Create an object
    # logger = logging.getLogger()

    # Now we are going to Set the threshold of logger to DEBUG
    globals.logger.setLevel(logging.DEBUG)

    # open Serial for COM 3 and baud rate 115200
    globals.ser

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
