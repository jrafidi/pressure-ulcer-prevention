from state import *
from accel import *
from bluepy.sensortag import *

import bluepy.btle as btle
import datetime, time, os

USB_PREFIX = '/media/'

# TODO: Read these addresses from a config file on the USB stick
LEFT_ADDRESS = 'BC:6A:29:AC:7F:1A'
RIGHT_ADDRESS = 'BC:6A:29:AE:CD:BB'

if __name__ == '__main__':
    # Turn off these debugging messages
    btle.Debugging = False

    # Find the USB stick and create data file for this boot
    try:
        usb = os.walk(USB_PREFIX).next()[1][0]
        file_prefix = USB_PREFIX + usb + '/pup-data/'
    # If there is no USB stick, just save it in the local directory
    except IndexError:
        file_prefix = 'local_data/'
    boot_time = str(datetime.datetime.today()).split('.')[0].replace(' ', '_').replace(':', '-')
    filename = file_prefix + 'data_' + boot_time + '.txt'
    data = file(filename, 'w')
    data.close()

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
        print 'ANGLE', calculateAngle(leftAccl, rightAccl)

        # Calculate posture state
        # Pass to state controller that will handle the rest
        time.sleep(5)
