from state import *
from accel import *
from indicators import *
from search import *
from bluepy.sensortag import *

import bluepy.btle as btle
import time, os

NUM_TAGS = 2

USB_PREFIX = '/media/'
LOCAL_PREFIX = '/home/pi/local-data/'

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
    blinkToggle = False

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

            # Find the sensortags
            [leftAddress, rightAddress] = findSensorTags()

            # Connect the TI sensor tags
            leftTag = SensorTag(leftAddress)
            rightTag = SensorTag(rightAddress)
            
            # Turn on the tag accelerometers
            tags = [leftTag, rightTag]
            for tag in tags:
                tag.accelerometer.enable()

            startConnection = False
            connected = True
            okayStatus()

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
            except btle.BTLEException:
                clearAll()
                errorStatus()
                triggerAlarm()

                connected = False
                startConnection = False

        if not connected and not startConnection:
            if blinkToggle:
                setOkay()
            else:
                clearOkay()
            blinkToggle = not blinkToggle

        time.sleep(DEFAULT_SPIN_TIME)
