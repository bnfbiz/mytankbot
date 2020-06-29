"""Servo Motor Support

This module provides basic support for managing an Servo motors for Raspberry Pi robots.
It provides the Servo class.


"""
import RPi.GPIO as GPIO
import time

class Servo:
    """Servo Class

    This class supports servo operations for the robot
    """
    #
    # Some useful information can be found:
    # https://howtomechatronics.com/how-it-works/how-servo-motors-work-how-to-control-servos-using-arduino/
    #
    def __init__(self, robot, servo_info_dict):
        """Initialize the Servo Motor

        ARGS
        servo_info_dict (dict): Dictionary containing the server motor information (servopin, frequency, minMilliSec, maxMillisec, maxDegrees)
        """
        try:
            if not robot.isInitialized():
                print("The robot is not initialized!")
                sys.exit(1)
        except:
            print("The robot is not initialized")
            sys.exit(1)

        # Setup the necessary values
        self.servoInfo = servo_info_dict
        self.minDutyCycle = self.servoInfo["minMilliSec"]/20*100
        self.maxDutyCycle = self.servoInfo["maxMilliSec"]/20*100
        self.maxDegrees = self.servoInfo["maxDegrees"]
        self.dutyCycleRange = self.maxDutyCycle - self.minDutyCycle

        # Set the operational range
        self.operMinDegrees = 0
        self.operMaxDegrees = self.servoInfo["maxDegrees"]

        # Initialize the servo
        GPIO.setup(self.servoInfo["servopin"],GPIO.OUT)
        self.servo = GPIO.PWM(self.servoInfo["servopin"], self.servoInfo["frequency"])
        self.servo.start(self.minDutyCycle) # Initialization

    def __del__(self):
        """Destructor

        Cleanup the servo
        """
        self.servo.stop()


    def servoSetOperationalRange(self, operMinDegrees,operMaxDegrees):
        """Set the range at which the servo should be operating within as it may be constrained"""
        if (operMinDegrees < 0):
            print("operMinDegrees out of range <0, setting to 0")
            self.operMinDegrees = 0
        else:
            self.operMinDegrees = operMinDegrees
        if (self.maxDegrees < operMaxDegrees):
            print("operMaxDegrees is out of range, it is greater than maxDegrees for the servo, setting to the max")
            self.operMaxDegrees = self.maxDegrees
        else:
            self.operMaxDegrees = operMaxDegrees

    def servoMoveDegrees(self, degrees):
        """Move the servo to the desired postion in degres"""
        if (degrees < self.operMinDegrees):
            print("Received a request to move to "+str(degrees)+", which is below the minimum value of "+str(self.operMinDegrees)+" setting to the minimum value!")
            degrees = self.operMinDegrees            
        elif (degrees > self.operMaxDegrees):
            print("Received a request to move to "+str(degrees)+", which is above the maximum value of "+str(self.operMaxDegrees)+" setting to the maximum value!")
            degrees = self.operMaxDegrees

        dutycycle = self.minDutyCycle + (self.dutyCycleRange * degrees/self.maxDegrees)
        if (dutycycle >= self.maxDutyCycle):
            dutycycle = self.maxDutyCycle

        self.servo.ChangeDutyCycle(dutycycle)
