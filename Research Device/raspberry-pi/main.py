from state import *
from accel import *
from indicators import *
from bluepy.sensortag import *

import bluepy.btle as btle
import time, os

USB_PREFIX = '/media/'
LOCAL_PREFIX = '/home/pi/local-data/'

# TODO: Read these addresses from a config file on the USB stick
LEFT_ADDRESS = 'BC:6A:29:AC:7F:1A'
RIGHT_ADDRESS = 'BC:6A:29:AE:CD:BB'

DEFAULT_SPIN_TIME = 1 #sec

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

    startConnection = False
    connected = False

    # Begin operating loop
    while True:
        # Check if the user has pushed the sync button
        if checkButton():
            startConnection = True
            connected = False
            clearAll()

        # Attempt to connect to the sensor tags
        if startConnection:
            # Reset all LEDs
            clearAll()
            # Reset the bluetooth junk in case something has gone wrong
            os.system('bash hci-reset.sh')

            # Connect the TI sensor tags
            leftTag = SensorTag(LEFT_ADDRESS)
            rightTag = SensorTag(RIGHT_ADDRESS)
            
            # Turn on the tag accelerometers
            tags = [leftTag, rightTag]
            for tag in tags:
                tag.accelerometer.enable()

            startConnection = False
            connected = True


        # Read accel data if connected
        if connected:
            try:
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
                time.sleep(SEC_PER_READING - DEFAULT_SPIN_TIME)
            except BTLEException:
                clearAll()
                errorStatus()
                triggerAlarm()

                connected = False
                startConnection = False

        time.sleep(DEFAULT_SPIN_TIME)
