from state import *
from bluepy.sensortag import *

import datetime, time, os

USB_PREFIX = '/media/'

if __name__ == '__main__':
    # Find the USB stick and create data file for this boot
    try:
        usb = os.walk(USB_PREFIX).next()[1][0]
        file_prefix = USB_PREFIX + usb + '/'
    except IndexError:
        file_prefix = 'local_data/'
    boot_time = str(datetime.datetime.today()).split('.')[0].replace(' ', '_').replace(':', '-')
    filename = file_prefix + 'data_' + boot_time + '.txt'
    data = file(filename, 'w')
    data.close()

    # Create the TI sensor tags
    tag1 = SensorTag("BC:6A:29:AC:7F:1A")
    tag2 = SensorTag("BC:6A:29:AE:CD:BB")

    sensors = [tag1.accelerometer, tag2.accelerometer]
    [ s.enable() for s in sensors ]

    # Create state obj
    while True:
        # Read accel data
        print "ACCL1", sensors[0].read()
        print "ACCL2", sensors[1].read()
        # Calculate posture state
        # Pass to state controller that will handle the rest
        print "TO DO"
