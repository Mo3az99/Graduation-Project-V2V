import socket
import globals
import FCA
import broadcast
import ICA
import car_controller
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
        print("not me")
        globals.logger.info(data_variable)
        FCA.determineLeadingVehicle(data_variable)
        print("am i following? ",globals.Following_vehicle)
        if globals.Following_vehicle:
            print("Iam Following and going to check a possible FCA")
            FCA.determineDistanceToCollison(data_variable)
        #Determine  if 2 directions will intersect
        #check direction
        if (globals.direction != data_variable["direction"] and globals.direction != "STOPPED" and data_variable["direction"] != "STOPPED"):
            print("going to check possiple intersection")
            #intersection point
            point_x, point_y = ICA.line_intersection(globals.line1, data_variable["line1"])
            dti_car1 = ICA.calculateDistance(point_x - globals.point2[0], point_y - globals.point2[1])
            #high possiblity for error
            dti_car2 = ICA.calculateDistance(point_x - data_variable["point1"][0], point_y - data_variable["point1"][1])
            tti_car1 = dti_car1 / 2.5 # instead of this put spead in meters
            tti_car2 = dti_car2 / 2.5 # instead of this put spead in meters
            print("my tti ",tti_car1)
            print("car2 tti",tti_car2)
            if (tti_car1 > tti_car2):
                # difference in time to not stop car if it will pass safely the intersection point
                if(abs(tti_car1-tti_car2) <= 5 ):
                    car_controller.Stop()
                    globals.stop=True
                    print("ICA STOOOOOOP")
                else:
                    globals.stop = False
                    print("ICA ez")
        elif globals.direction == data_variable["direction"]:
            globals.stop = False


        # print(data_variable.locationx)
        # (data, addr) = rev_socket.recvfrom(SIZE)
        # data1 = data.decode('utf-8')
        # print(data1 + " From	" + str(addr) + "\n")