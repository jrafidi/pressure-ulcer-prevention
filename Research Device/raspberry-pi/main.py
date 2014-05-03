from state import *
from accel import *
from bluepy.sensortag import *

import bluepy.btle as btle
import time, os

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

USB_PREFIX = '/media/'
LOCAL_PREFIX = 'local_data/'

# TODO: Read these addresses from a config file on the USB stick
LEFT_ADDRESS = 'BC:6A:29:AC:7F:1A'
RIGHT_ADDRESS = 'BC:6A:29:AE:CD:BB'

if __name__ == '__main__':
    # Turn off these debugging messages
    btle.Debugging = False

    # Find the USB stick if available
    try:
        usb = os.walk(USB_PREFIX).next()[1][0]
        storage_prefix = USB_PREFIX + usb + '/pup-data/'
    except IndexError:
        storage_prefix = None

    # Create the state controller
    state = ModuleStateController(LOCAL_PREFIX, storage_prefix)

    # Connect the TI sensor tags
    leftTag = SensorTag(LEFT_ADDRESS)
    rightTag = SensorTag(RIGHT_ADDRESS)

    tags = [leftTag, rightTag]
    for tag in tags:
        tag.accelerometer.enable()

    # Create state obj
    while True:
        # Read accel data
        leftAccl = leftTag.accelerometer.read()
        rightAccl = rightTag.accelerometer.read()
        print 'LEFT_ACCL', leftAccl
        print 'RIGHT_ACCL', rightAccl

        # Calculate posture state (TODO)
        angle = calculateAngle(leftAccl, rightAccl)
        sleeping = False
        print 'ANGLE', calculateAngle(leftAccl, rightAccl)
        print 'SLEEPING', sleeping

        # Pass to state controller that will handle the rest
        state.updateState(angle, sleeping)

        # Wait to take the next reading
        time.sleep(SEC_PER_READING)
