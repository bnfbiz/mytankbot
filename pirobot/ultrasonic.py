"""Ultrasonic Sensor Support

This module provides basic support for managing an ultrasonic sensorfor Raspberry Pi robots, It provides the Ultrasonic class.

"""
import RPi.GPIO as GPIO
import time


SPEED_OF_SOUND_cMPerS = 343 * 100  # 100cm per meter
SPEED_OF_SOUND_inPerS = 13503.9

UNITS_CM = "cm"
UNITS_IN = "in"

class Ultrasonic:
    """Ultrasonic Class

        This class supports ultrasonic operations for the robot
    """

    DEFAULT_TRIGGER_TIME = 0.00002
    UNITS_CM = "cm"
    UNITS_IN = "in"

    def __init__(self):
        """Constructor
        
        Initialize the Ultrasonic class, currently takes no inputs
        """
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)

    def __del__(self):
        """Destructor

        Cleanup the GPIO inputs
        """
        pass

    def init_us(self, ultrasonice_sensor_dict, trigger_time = DEFAULT_TRIGGER_TIME, units=UNITS_CM):
        """Initialize the Ultrasonic Sensor

        ARGS
        ultrasonic_sensor_dict (dict): Dictionary containing the echopin and triggerpin settings
        trigger_time (float):          The time to wait before watching for the echo response.  Default is 0.00002
        units (string):                The units to measure the distance in, values are "cm" or "in", Default is "cm"
        """
        self.uss = ultrasonice_sensor_dict
        self.trigger_time = trigger_time
        self.us_units = units
        if self.us_units == UNITS_CM:
            self.speed_of_sound = SPEED_OF_SOUND_cMPerS
        else:
            self.speed_of_sound = SPEED_OF_SOUND_inPerS

        # Setup Ultrasonic Sensor
        GPIO.setup(self.uss["triggerpin"],GPIO.OUT)
        GPIO.setup(self.uss["echopin"],GPIO.IN)

        # Initialize to no echoing
        GPIO.output(self.uss["triggerpin"],GPIO.LOW)

    def GetDistanceUsonic(self):
        """Returns a float with the distance"""
        GPIO.output(self.uss["triggerpin"],GPIO.HIGH)
        time.sleep(self.trigger_time)
        GPIO.output(self.uss["triggerpin"],GPIO.LOW)

        # Determine when the ping starts
        echo_start = time.time()
        while GPIO.input(self.uss["echopin"]) == 0:
            echo_start = time.time()
        
        # wait until ping ends
        while GPIO.input(self.uss["echopin"]) == 1:
            echo_stop = time.time()

        # turn off the echo to get rid of the occassional hang
        GPIO.output(self.uss["triggerpin"],GPIO.LOW)

        echo_duration = echo_stop - echo_start

        #          Distance
        # Speed = ----------   ==> Distance = Speed * Time / 2
        #           Time/2
        # Time is divided by 2 as it is a round trip
        #
        distance = self.speed_of_sound * echo_duration / 2
        return(distance)
