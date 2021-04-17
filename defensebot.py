#!/usr/bin/env python3

import serial
import time
from pirobot import joystick, robot, solenoid

shifter_solenoid = {"pin": 4}
print ("Setup")
robot = robot.Robot()
joystick = joystick.Joystick("gamepad")
joystick.setAxisRange(lower_limit=0, upper_limit=180)

# Setup the Servo Motor for the ultrasonic Sensor
solenoid = solenoid.Solenoid(robot)
solenoid.init_solenoid(shifter_solenoid, solenoid.LOW)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
    ser.flush()
    left_y_axis = 90
    right_y_axis = 90
    data="P03 90 P05 90 P09 90 P10 90"
    l_data = "P03 90"
    r_data = ""
    count = 0
    buttons = [311]
    try:
        while 1:
            new_left_y_axis = joystick.getAxisValueRange(joystick.LY_AXIS)
            new_right_y_axis = joystick.getAxisValueRange(joystick.RY_AXIS)
            keys = joystick.active_keys(verbose=True)
 
            # check to see if RB (311) or LB (310) is pressed, if so reverse the solenoid
            if (310 in keys):
                print("Setting low")
                solenoid.set(solenoid.LOW)

            if (311 in keys):
                print("Setting High")
                solenoid.set(solenoid.HIGH)
                
            if (new_left_y_axis != left_y_axis):
                left_y_axis = new_left_y_axis
                # invert the motors
                inverted = abs(180 - int(left_y_axis))
                l_data ="P03 " + str(inverted)
                l_data +=" P05 " + str(inverted)
                count = 0
            if (new_right_y_axis != right_y_axis):
                right_y_axis = new_right_y_axis
                r_data ="P09 " + str(int(right_y_axis))
                r_data +=" P10 " + str(int(right_y_axis))
                count = 0

            if (count == 0):
                print("Data to send:" + data)
                data = l_data + " " + r_data
                ser.reset_output_buffer()
                ser.write(bytes(data,'utf-8'))
            
            if (ser.inWaiting() > 0):
                line = ser.readline().decode('utf-8').rstrip()
                print("received: " + line)
            count = (count + 1) % 14
            time.sleep(0.1)

            
    except KeyboardInterrupt:
        pass

    del joystick

