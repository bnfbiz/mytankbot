import time
from pirobot import robot, joystick, ultrasonic

# Definition of motor pin (BOARD)
left_motor = {"forwardpin": 20, "backwardpin": 21, "speedpin": 16}
right_motor = {"forwardpin": 19, "backwardpin": 26, "speedpin": 13}

# Definition of ultrasonic pin (BOARD)
echo_pin = 0
trigger_pin = 1

print ("Setup")
robot = robot.Robot()
robot.inittank(left_motor,right_motor)
joystick = joystick.Joystick("gamepad")
joystick.setAxisRange(lower_limit=-100, upper_limit=100)
ultrasonic = ultrasonic.Ultrasonic()
ultrasonic = ultrasonic.init_us(echo_pin, trigger_pin, ultrasonic.DEFAULT_TRIGGER_TIME, ultrasonic.UNITS_CM)

try:
    while 1:
        left_y_axis = joystick.getAxisValueRange(joystick.LY_AXIS)
        right_y_axis = joystick.getAxisValueRange(joystick.RY_AXIS)
        robot.move(left_y_axis,right_y_axis)
        
except KeyboardInterrupt:
    pass

del robot

