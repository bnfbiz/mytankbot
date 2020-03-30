import time
import robotpackage

# Definition of motor pin (BOARD)
left_motor = {"forwardpin": 38, "backwardpin": 40, "speedpin": 36}
right_motor = {"forwardpin": 35, "backwardpin": 37, "speedpin": 33}

print ("Setup")
robot = robotpackage.robot.Robot()
robot.inittank(left_motor,right_motor)
joystick = robotpackage.joystick.Joystick("gamepad")
joystick.setAxisRange(lower_limit=-100, upper_limit=100)

try:
    while 1:
        left_y_axis = joystick.getAxisValueRange(robotpackage.joystick.LY_AXIS)
        right_y_axis = joystick.getAxisValueRange(robotpackage.joystick.RY_AXIS)
        robot.move(left_y_axis,right_y_axis)
        
except KeyboardInterrupt:
    pass

del robot

