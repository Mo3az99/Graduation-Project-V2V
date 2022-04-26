
import socket
import globals
import FCA

def receive():

    #global SIZE
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