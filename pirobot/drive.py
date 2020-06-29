"""Robot Drive Support

This module provides basic driving support for Raspberry Pi robots, currently the only drive support is for a 
tank based robot.   It provides the Robot class.

"""
import RPi.GPIO as GPIO
import sys
import time

class Drive:
    """Drive Class

    This class supports driving operations for the robot
    """

    def __init__(self, robot):
        """Constructor

        Initialize the Drive class.  Currently takes no parameters.
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

        Cleanup the robot and GPIO settings
        """
        try:
            self.pwm_lms.stop(0)
            self.pwm_rms.stop(0)
        except AttributeError:
            pass

        GPIO.cleanup()

    def init_tank(self, leftmotor_dict, rightmotor_dict):
        """Initiailize the tank robot

        Args:
            leftmotor_dict (dict):  Dictionary containing the Forward, Backward and Speed PINs for the left motor
            rightmotor_dict (dict): Dictionary containing the Forward, Backward and Speed PINs for the right motor
        """
        self.lm = leftmotor_dict
        self.rm = rightmotor_dict
        # Setup left motor
        GPIO.setup(self.lm["speedpin"],GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.lm["forwardpin"],GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.lm["backwardpin"],GPIO.OUT,initial=GPIO.LOW)
        self.pwm_lms = GPIO.PWM(self.lm["speedpin"], 2000)
        # Setup right motor
        GPIO.setup(self.rm["speedpin"],GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.rm["forwardpin"],GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.rm["backwardpin"],GPIO.OUT,initial=GPIO.LOW)
        self.pwm_rms = GPIO.PWM(self.rm["speedpin"], 2000)

        # set the motors to be off
        self.pwm_lms.start(0)
        self.pwm_rms.start(0)

    def move(self, leftmagnitude, rightmagnitude):
        """

        Args:
            leftmagnitude (float):  Magnitude of the left motor (range -100 to 100)
            rightmagnitude (float): Magnitude of the right motor (range -100 to 100)
        """
        if leftmagnitude > 0:
            GPIO.output(self.lm["forwardpin"], GPIO.LOW)
            GPIO.output(self.lm["backwardpin"], GPIO.HIGH)
        elif leftmagnitude < 0:
            GPIO.output(self.lm["forwardpin"], GPIO.HIGH)
            GPIO.output(self.lm["backwardpin"], GPIO.LOW)
        else:
            GPIO.output(self.lm["forwardpin"], GPIO.LOW)
            GPIO.output(self.lm["backwardpin"], GPIO.LOW)
        if rightmagnitude > 0:
            GPIO.output(self.rm["forwardpin"], GPIO.LOW)
            GPIO.output(self.rm["backwardpin"], GPIO.HIGH)
        elif rightmagnitude < 0:
            GPIO.output(self.rm["forwardpin"], GPIO.HIGH)
            GPIO.output(self.rm["backwardpin"], GPIO.LOW)
        else:
            GPIO.output(self.rm["forwardpin"], GPIO.LOW)
            GPIO.output(self.rm["backwardpin"], GPIO.LOW)

        # ensure the magnitude is in range
        leftmagnitude = abs(leftmagnitude)
        leftmagnitude = leftmagnitude if leftmagnitude < 100 else 100
        rightmagnitude = abs(rightmagnitude)
        rightmagnitude = rightmagnitude if rightmagnitude < 100 else 100
        self.pwm_lms.ChangeDutyCycle(leftmagnitude)
        self.pwm_rms.ChangeDutyCycle(rightmagnitude)
