import socket
import time
import threading
#import io
import pynmea2
import serial


# add Semaphore for Location
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
    print(location)
    msg = pynmea2.parse(location)
    # improve convert msg.lat
    var_Location = (str(convert_lat(msg.lat)) +" °"+ msg.lat_dir +", "+str(convert_long(msg.lon)) + " °"+ msg.lon_dir )
    #print(msg.lon)
    print(getlocation_link(convert_lat(msg.lat), convert_long(msg.lon)))


def send():
    # location = getlocation()
    # sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    # nazlha ta7t 34an mkan el kolya et3ml update
    current_location()

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    #send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    send_socket.settimeout(0.2)
    message = str.encode("PC Location " + var_Location)
    while True:
        send_socket.sendto(message, ('<broadcast>', 5037))
        print("message sent! \n")
        #Sleep for 1 second
        time.sleep(1)


def receive():
    PORT_NUMBER = 5037
    SIZE = 1024

    hostName = socket.gethostbyname('0.0.0.0')
    rev_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rev_socket.bind((hostName, PORT_NUMBER))
    print("Test server listening on port {0}\n".format(PORT_NUMBER))
    # rev_socket.connect(('192.168.60.77', 5037))
    #rev_socket.bind(('192.168.60.77', PORT_NUMBER))
#    print("Test server listening on port {0}\n".format(PORT_NUMBER))

    while True:
        (data, addr) = rev_socket.recvfrom(SIZE)
        data1 = data.decode('utf-8')
        print(data1 + " From	" + str(addr) +"\n")


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
    degree =float(str(x)[:2])
    minutes =float(str(x)[2:])
    result = degree+(minutes/60)
    return result
def getlocation_link(lat,lon):
    link = "http://maps.google.com/maps?q=loc:" + str(lat) + ","+str(lon)
    return link

def convert_long(x):
    degree =float(str(x)[:3])
    minutes =float(str(x)[3:])
    result = degree+(minutes/60)
    return result

def send_message(number, message):
    print(number)
    print(message)
    ser.write(b'AT \r\n')  # check the GSM+GPRS module, should return OK if working
    receive = ser.read(100)
    print(receive)
    time.sleep(1)
    ser.write(b'AT+CMGF=1 \r\n')  # set to text mode
    receive = ser.read(100)
    print(receive)
    time.sleep(1)
    AT_number = 'AT+CMGS="{}"'.format(number) + '\r\n'
    ser.write(str.encode(AT_number))  # the number where message is to be sent
    receive = ser.read(100)
    print(receive)
    time.sleep(1)
    ser.write(message.encode('utf-8'))  # the message text
    ser.write('\r\n'.encode('utf-8'))
    receive = ser.read(100)
    print(receive)
    ser.write(b'\x1A')
    for i in range(10):
        receive = ser.read(1000)  # read the response from the service provider if additional information sent
        print(receive)

if __name__ == "__main__":
    # creating threads
    rev_thread = threading.Thread(target=receive)
    # send_thread = threading.Thread(target=send)

    # open Serial for COM 3 and baud rate 115200
    # ser = serial.Serial('COM3', 115200, timeout=1)
    # send_message("01115345676", "V2V")
    # initialize GPS
    # init()

    # starting thread 1 for Receiving
    rev_thread.start()
    # starting thread 2 Main Thread
    # send_thread.start()


