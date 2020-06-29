"""Robot Platform Support

This module provides hardware setup for Raspberry Pi robots.  It provides the Robot class.

"""
import RPi.GPIO as GPIO
import time

class Robot:
    """Robot Class

    This class supports basic HW setup operations for the robot
    """

    initialized = False

    def __init__(self):
        """Constructor

        Initialize the Robot class.  Currently takes no parameters.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.initialized = True

    def __del__(self):
        """Destructor

        Cleanup the robot and GPIO settings
        """
        self.pwm_lms.stop(0)
        self.pwm_rms.stop(0)
        GPIO.cleanup()
        self.initialized = False

    def isInitialized(self):
        """is the robot Initialized"""
        return self.initialized
    