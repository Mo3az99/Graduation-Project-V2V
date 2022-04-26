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

def receive():

    hostName = socket.gethostbyname('0.0.0.0')
    rev_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rev_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    rev_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rev_socket.bind((hostName, globals.PORT_NUMBER))
    print("Test server listening on port {0}\n".format(globals.PORT_NUMBER))
    while True:
        data_encoded = rev_socket.recv(8192)
        data_string = data_encoded.decode(encoding="utf-8")
        data_variable = globals.json.loads(data_string)
        # logger.info(data_variable)
        if data_variable["vecid"] == globals.vecid:
           continue
        globals.logger.info(data_variable)
        FCA.determineLeadingVehicle(data_variable)
        if globals.Following_vehicle:
            print("Iam Following and going to check a possible FCA")
            FCA.determineDistanceToCollison(data_variable)

        # print(data_variable.locationx)
        # (data, addr) = rev_socket.recvfrom(SIZE)
        # data1 = data.decode('utf-8')
        # print(data1 + " From	" + str(addr) + "\n")


# Function to get the Current Location from current_Location function and update the Global Location Variable
# preparing the socket for broadcasting and reusing the port
# finally we broadcast the location over the network and printing an Acknowledgement message
def broadcast():
    # location = getlocation()
    # sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    # nazlha ta7t 34an mkan el kolya et3ml update
    # current_location()

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    send_socket.settimeout(0.2)
    broadcast.current_location()
    broadcast.update_speed()
    broadcast.update_angle()
    broadcast.update_acceleration()
    bcn1 = Kalman.bcnSample(globals.vecid, 0, globals.locationx, globals.locationy, globals.velocityx,globals.velocityy)
    klm = Kalman.kalmanTrack(bcn1, 0)
    while True:
        broadcast.current_location()
        klm.predict()
        bcn1 = Kalman.bcnSample(globals.vecid, 0, globals.locationx, globals.locationy, globals.velocityx, globals.velocityy)
        klm.update(bcn1, 1)
        globals.locationx = klm.X[0]
        globals.locationy = klm.X[3]

        broadcast.update_speed()
        globals.velocityx=klm.X[1]
        globals.velocityy=klm.X[4]
        broadcast.update_angle()
        #keda ba3d kalman should be deleted after test
        broadcast.update_acceleration()
        #add kalman
        #send kalman cooridantes
        globals.acceleration = math.sqrt(math.pow(klm.X[2], 2) + math.pow(klm.X[5], 2))
        variable = message(globals.vecid, klm.X[0], klm.X[3], klm.X[1], klm.X[4], globals.acceleration, globals.stop, globals.angle, globals.direction)
        # Map your object into dict
        data_as_dict = vars(variable)

        # Serialize your dict object
        data_string = json.dumps(data_as_dict)
        send_socket.sendto(data_string.encode(encoding="utf-8") , ('<broadcast>',5037))
        globals.logger.info(data_as_dict)
        #tayha fl logger deh
        # send_socket.sendto(message, ('<broadcast>', 5037))
        print("message sent! \n")
        # Sleep for 1 second
        time.sleep(1)

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
                if stop == False:
                    if globals.UP_Pressed and globals.Right_Pressed:
                        print("Right Forward")
                        car_controller.up_right()
                    elif globals.UP_Pressed and globals.Left_Pressed:
                        print("left forward")
                        car_controller.up_left()
                    elif globals.Down_Pressed and globals.Right_Pressed:
                        print("backward right")
                        car_controller.down_right()
                    elif globals.Down_Pressed and globals.Left_Pressed:
                        print("backward Left")
                        car_controller.down_left()
                    elif globals.UP_Pressed:
                        print("Move Forward")
                        car_controller.up()
                    elif globals.Down_Pressed:
                        print("Move Backward")
                        car_controller.down()
                    elif globals.Right_Pressed:
                        print("Move Right")
                        car_controller.right()
                    elif globals.Left_Pressed:
                        print("Move Left")
                        car_controller.left()
                    else:
                        print("Stop")
                        Stop()
            except Exception as e:
                print(e)
                print("break")


#functionality of the Ultrasonic
def ultrasonic():

    try:
        while True:
            dist = ultrasonic.distance()
            if dist < 50:
                print("Warning")
                car_controller.Stop()
                globals.stop = True
            else:
                globals.stop = False
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


if __name__ == "__main__":
    # creating threads
    rev_thread = threading.Thread(target=receive())
    broadcast_thread = threading.Thread(target=broadcast())
    Car_thread = threading.Thread(target=car_Controller())
    Ultrasonic_thread = threading.Thread(target=ultrasonic())
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
