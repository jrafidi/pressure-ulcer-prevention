from state import *

import datetime
import os

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

    # Create state obj
    while True:
        # Read accel data
        # Calculate posture state
        # Pass to state controller that will handle the rest
        print "TO DO"
