"""Line Tracker Support

This module provides basic support for managing a Line traker for Raspberry Pi robots.
It provides the LineSensor class.


"""
import RPi.GPIO as GPIO
import time

class LineSensor:
    """LineSensor Class

    This class supports LineTracking operations for the robot
    """
    def __init__(self, robot):
        """Constructor
        
        Initialize the LineSensor class, currently takes no inputs
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

        Cleanup the Line Tracker Sensor
        """
        pass

    def init_line_sensor(self, line_tracker_dict):
        """Initialize a Line Tracker with the list of inputs

        ARGS
        line_tracker_dict (dict): Dictionary containing the Line Tracker information (line tracker pins and names)
        """
        # Setup the necessary values
        self.ltInfo = line_tracker_dict
        
        # Initialize the Line Tracker
        for k in self.ltInfo.keys():
            GPIO.setup(self.ltInfo[k],GPIO.IN)
        
    def getLineSensor(self):
        """Get the status of the line sensors"""

        sensorInputs = {}
        val = False
        anyFound = False

        for k in self.ltInfo.keys():
            val = GPIO.input(self.ltInfo[k])
            sensorInputs[k] = val
            if val == 0:
                anyFound = True
        
        sensorInputs["anyFound"] = anyFound
        return(sensorInputs)

    