"""Robot Drive Support

This module provides basic driving support for Raspberry Pi robots, currently the only drive support is for a 
tank based robot.   It provides the Robot class.

"""
import RPi.GPIO as GPIO
import time

SPEED_OF_SOUND_cMPerS = 343 * 100  # 100cm per meter
SPEED_OF_SOUND_inPerS = 13503.9

UNITS_CM = "cm"
UNITS_IN = "in"

class Robot:
    """Robot Class

    This class supports driving operations for the robot
    """
    
    DEFAULT_TRIGGER_TIME = 0.00002
    UNITS_CM = "cm"
    UNITS_IN = "in"

    def __init__(self):
        """Constructor

        Initialize the robot class.  Currently takes no parameters.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def __del__(self):
        """Destructor

        Cleanup the robot and GPIO settings
        """
        self.pwm_lms.stop(0)
        self.pwm_rms.stop(0)
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

    #
    # The following methods are for Servos
    #
    def init_servo(self, servo_info_dict):
        """Initialize the Servo Motor

        ARGS
        servo_info_dict (dict): Dictionary containing the server motor information (servopin, frequency, minMilliSec, maxMillisec)
        """
        # Setup the necessary values
        self.servoInfo = servo_info_dict
        self.minDutyCycle = self.servoInfo["minMilliSec"]/20*100
        self.maxDutyCycle = self.servoInfo["maxMilliSec"]/20*100
        self.maxDegrees = self.servoInfo["maxDegrees"]
        self.dutyCycleRange = self.maxDutyCycle - self.minDutyCycle

        # Initialize the servo
        GPIO.setup(self.servoInfo["servopin"],GPIO.OUT)
        self.servo = GPIO.PWM(self.servoInfo["servopin"], self.servoInfo["frequency"])
        self.servo.start(self.minDutyCycle) # Initialization

    def servoMoveDegrees(self, degrees):
        """Move the servo to the desired postion in degres"""
        if (degrees <= self.maxDegrees):
            dutycycle = self.minDutyCycle + (self.dutyCycleRange * degrees/self.maxDegrees)
            
            if (dutycycle >= self.maxDutyCycle):
                dutycycle = self.maxDutyCycle
        else:
            dutycycle = self.maxDutyCycle
        self.servo.ChangeDutyCycle(dutycycle)

    # 
    # The following methods are for the Ultrasonic Sensor
    #
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