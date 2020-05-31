import time
from pirobot import robot, joystick

# Definition of motor pin (BCM)
left_motor = {"forwardpin": 20, "backwardpin": 21, "speedpin": 16}
right_motor = {"forwardpin": 19, "backwardpin": 26, "speedpin": 13}
ultrasonic_sensor = {"echopin": 0, "triggerpin": 1}
ultrasonic_servo = {"servopin": 23, "frequency": 50, "minMilliSec": 0.5, "maxMilliSec": 2.5, "maxDegrees": 180}

print ("Setup")
robot = robot.Robot()
robot.init_tank(left_motor,right_motor)
joystick = joystick.Joystick("gamepad")
joystick.setAxisRange(lower_limit=-100, upper_limit=100)
robot.init_us(ultrasonic_sensor, robot.DEFAULT_TRIGGER_TIME, robot.UNITS_CM)
robot.init_servo(ultrasonic_servo)

angle = 0
count_up = True

try:
    while 1:
        left_y_axis = joystick.getAxisValueRange(joystick.LY_AXIS)
        right_y_axis = joystick.getAxisValueRange(joystick.RY_AXIS)
        robot.move(left_y_axis,right_y_axis)
        robot.servoMoveDegrees(angle)
        if angle > ultrasonic_servo["maxDegrees"]:
            count_up = False
        elif  angle < 0:
            count_up = True

        if count_up:
            angle += 1
        else:
            angle -= 1

        distance = robot.GetDistanceUsonic()
        print("Distance is " + str(distance))

        
except KeyboardInterrupt:
    pass

del robot

