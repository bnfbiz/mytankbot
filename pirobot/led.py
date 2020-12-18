"""LED Support

This module provides basic support for managing an LEDs for Raspberry Pi robots.
It provides the LED class.


"""
import RPi.GPIO as GPIO
import time

class LED:
    """LED Class

    This class supports LED operations for the robot
    """
    def __init__(self, robot):
        """Constructor
        
        Initialize the LED class, currently takes no inputs
        """
        try:
            if not robot.isInitialized():
                print("The robot is not initialized!")
                sys.exit(1)
        except:
            print("The robot is not initialized")
            sys.exit(1)

    def __del__(self):
        """Destructor

        Cleanup the LEDs
        """
        pass

    def init_led(self, led_info_dict):
        """Initialize a LED

        ARGS
        led_info_dict (dict): Dictionary containing the LED information (ledpin)
        """
        # Setup the necessary values
        self.ledInfo = led_info_dict
        
        # Initialize the LED
        GPIO.setup(self.ledInfo["ledpin"],GPIO.OUT)
        
    def setLED(self, val):
        """Turn On/Off the LED"""
        if (val == True):
            GPIO.output(self.ledInfo["ledpin"],GPIO.HIGH)
        else:
            GPIO.output(self.ledInfo["ledpin"],GPIO.LOW)

    