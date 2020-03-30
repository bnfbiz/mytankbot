
import evdev

LX_AXIS=evdev.ecodes.ABS_X
LY_AXIS=evdev.ecodes.ABS_Y
RX_AXIS=evdev.ecodes.ABS_RX
RY_AXIS=evdev.ecodes.ABS_RY

class Joystick:
    def __init__(self,deviceString = ""):
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
        return self.device.absinfo(axis_num)

    def active_keys(self, verbose=False):
        return self.device.active_keys()

    def capabilities(self, verbose=False, absinfo=True):
        return self.device.capabilities(verbose=verbose, absinfo=absinfo)

    def setAxisRange(self, lower_limit=-1, upper_limit = 1, deadband = .1):
        self.llimit = lower_limit
        self.ulimit = upper_limit
        self.deadband = deadband

    def getAxisValueRange(self, axis):
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