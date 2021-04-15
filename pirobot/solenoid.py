"""Solenoid Support

This module provides basic support for managing an solenoids for Raspberry Pi robots.
It provides the Solenoid class.


"""
import RPi.GPIO as GPIO
import time
import sys

class Solenoid:
    """Solenoid Class

    This class supports solenoid operations for the robot
    """
    HIGH = GPIO.HIGH
    LOW = GPIO.LOW
    def __init__(self, robot):
        """Initialize the Solenoid

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

        Cleanup the solenoid
        """
        pass

    def init_solenoid(self, solenoid_info_dict, initial_state):
        """Initialize the solenoid Sensor

        ARGS
        selenoid_info_dict (dict):     Dictionary containing the solenoid information (pin)
        initial_state (int):           The initial state to set the port to
        """
        # Setup the necessary values
        self.solenoidInfo = solenoid_info_dict
        self.pin = self.solenoidInfo["pin"]

        # Initialize the solenoid and set the initial state
        GPIO.setup(self.solenoidInfo["pin"],GPIO.OUT)
        GPIO.output(self.solenoidInfo["pin"],initial_state)

    def set(self, state):
        """Initialize the solenoid Sensor

        ARGS
        state (int):           The state to set the port to
        """
        # set the solenoid state
        GPIO.output(self.solenoidInfo["pin"],state)