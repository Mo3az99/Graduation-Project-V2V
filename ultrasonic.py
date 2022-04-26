import car_controller
import time
import RPi.GPIO as GPIO
import globals
#Calculate Distance with Ultrasonic
def distance():
    # set Trigger to HIGH
    GPIO.output(globals.GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(globals.GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(globals.GPIO_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(globals.GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

#functionality of the Ultrasonic
def ultrasonic():

    try:
        while True:
            dist = distance()
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