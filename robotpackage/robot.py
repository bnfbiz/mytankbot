import RPi.GPIO as GPIO
import time

class Robot:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def __del__(self):
        self.pwm_lms.stop(0)
        self.pwm_rms.stop(0)
        GPIO.cleanup()

    def inittank(self, leftmotor_dict, rightmotor_dict):
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

