"""Joystick Support

This module provides joystick support for Raspberry Pi robots.   It provides the Joystick class.

"""


import evdev

class Joystick:
    """Joystick Class

    This class supports joystick operations for the robot
    """

    LX_AXIS=evdev.ecodes.ABS_X
    LY_AXIS=evdev.ecodes.ABS_Y
    RX_AXIS=evdev.ecodes.ABS_RX
    RY_AXIS=evdev.ecodes.ABS_RY

    def __init__(self, deviceString = ""):
        """Constructor
        
        Can be intialized with a component of the device path or string such as 
        `Logitech Gamepade F710` or substring such as `gamepad`. The device string is converted to lower case
        for the comparision.

        Args:
            deviceString (str): The joystick device to initialize
        """
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for dev in devices:
            # print(dev.path, dev.name, dev.phys)
            if deviceString in dev.name.lower():
                self.devicePath = dev.path
                print("Found the " + deviceString + " at " + self.devicePath)

            if len(self.devicePath) <= 0:
                print("Unable to determine the gamepad")
                exit(1)

        self.device = evdev.InputDevice(self.devicePath)
        print ("name: ")
        print(self.device.name)

    def absinfo(self, axis_num):
        """Returns the AXIS of the ABS Axis number"""
        return self.device.absinfo(axis_num)

    def active_keys(self, verbose=False):
        """Returns the active joystick buttons"""
        return self.device.active_keys()

    def capabilities(self, verbose=False, absinfo=True):
        """Returns the capabilities of the controller"""
        return self.device.capabilities(verbose=verbose, absinfo=absinfo)

    def setAxisRange(self, lower_limit=-1, upper_limit = 1, deadband = .1):
        """Set the axis range of the joystick"""
        self.llimit = lower_limit
        self.ulimit = upper_limit
        self.deadband = deadband

    def getAxisValueRange(self, axis):
        """Gets the axis value mapped to the axis range set by setAxisRange()"""
        actual, min, max, fuzz, flat, res = self.absinfo(axis)
        
        deadband_range = round((max - min)/2 * self.deadband)
        middle_source = (max + min) / 2
        middle_dest = (self.ulimit + self.llimit) / 2
        if abs(actual) > deadband_range:
            # map between the joystick min/max to the requested lower/upper values
            if actual < middle_source:
                # lower range
                source_ratio = (actual - middle_source)/min
                dest_ratio = (source_ratio * (self.llimit - middle_dest)) + middle_dest
            else:
                # upper range
                source_ratio = (actual - middle_dest)/max
                dest_ratio = (source_ratio * (self.ulimit - middle_dest)) + middle_dest
        else:
            # in the deadband range so return the middle of the range requested
            dest_ratio = middle_dest
        return dest_ratio

if __name__ == "__main__":
    print(__doc__)
    print(Joystick.__doc__)