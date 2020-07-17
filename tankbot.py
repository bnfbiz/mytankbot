import time
from pirobot import drive, led, joystick, linesensor, robot, servo, ultrasonic

# Definition of motor pin (BCM)
left_motor = {"forwardpin": 20, "backwardpin": 21, "speedpin": 16}
right_motor = {"forwardpin": 19, "backwardpin": 26, "speedpin": 13}
ultrasonic_sensor = {"echopin": 0, "triggerpin": 1}
ultrasonic_servo = {"servopin": 23, "frequency": 50, "minMilliSec": 0.5, "maxMilliSec": 2.5, "maxDegrees": 180}
camera_servo_lr = {"servopin": 11, "frequency": 50, "minMilliSec": 0.5, "maxMilliSec": 2.5, "maxDegrees": 180}
camera_servo_ud = {"servopin": 9, "frequency": 50, "minMilliSec": 0.5, "maxMilliSec": 2.5, "maxDegrees": 180}
line_sensor = {"farLeft": 3, "middleLeft": 5, "middleRight": 4, "farRight": 18}

red_led = {"ledpin": 22}
green_led = {"ledpin": 27}
blue_led = {"ledpin": 24}

print ("Setup")
robot = robot.Robot()
drive = drive.Drive(robot)
drive.init_tank(left_motor,right_motor)

joystick = joystick.Joystick("gamepad")
joystick.setAxisRange(lower_limit=-100, upper_limit=100)

# Setup the Ultrasonic Sensor
ultrasonic = ultrasonic.Ultrasonic(robot)
ultrasonic.init_us(ultrasonic_sensor, ultrasonic.DEFAULT_TRIGGER_TIME, ultrasonic.UNITS_CM)

# Setup the Servo Motor for the ultrasonic Sensor
us_servo = servo.Servo(robot, ultrasonic_servo)

# # Setup the line sensor
# line = linesensor.LineSensor(robot)
# line.init_line_sensor(line_sensor)

# Setup the camera mount
camera_lr = servo.Servo(robot, camera_servo_lr)
camera_ud = servo.Servo(robot, camera_servo_ud)
camera_ud.servoSetOperationalRange(30,140)
camera_lr.servoMoveDegrees(90)
camera_ud.servoMoveDegrees(80)

# Initialize the LED's
redLed = led.LED(robot)
redLed.init_led(red_led)
greenLed = led.LED(robot)
greenLed.init_led(green_led)
blueLed = led.LED(robot)
blueLed.init_led(blue_led)

angle = 0
count_up = True

try:
    while 1:
        left_y_axis = joystick.getAxisValueRange(joystick.LY_AXIS)
        right_y_axis = joystick.getAxisValueRange(joystick.RY_AXIS)
        drive.move(left_y_axis,right_y_axis)
        # print("Line sensor is ",line.getLineSensor())
        us_servo.servoMoveDegrees(angle)

        if angle >= ultrasonic_servo["maxDegrees"]:
            count_up = False
        elif angle <= 0:
            count_up = True

        if count_up:
            angle += 1
        else:
            angle -= 1

        distance = ultrasonic.GetDistanceUsonic()
        # print("Distance is " + str(distance))
        if distance > 200:
            redLed.setLED(True)
            greenLed.setLED(False)
            blueLed.setLED(False)
        elif distance > 100:
            redLed.setLED(False)
            greenLed.setLED(False)
            blueLed.setLED(True)
        else:
            redLed.setLED(False)
            greenLed.setLED(True)
            blueLed.setLED(False)

        time.sleep(0.05)

        
except KeyboardInterrupt:
    pass

del line
del camera_lr
del camera_ud
del redLed
del greenLed
del blueLed
del us_servo
del ultrasonic
del joystick
del robot

