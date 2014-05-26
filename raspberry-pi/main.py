from state import *
from accel import *
from indicators import *
from search import *
from bluepy.sensortag import *

import bluepy.btle as btle
import time, os

NUM_TAGS = 3

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

    connected = False
    calibrated = False
    blinkToggle = False

    # Begin operating loop
    while True:
        # Check if the user has pushed the sync button
        if checkButton() and not connected and not startConnection and not calibrated:
            clearAll()
            connected = False

            # Find the sensortags
            [addr1, addr2, addr3] = findSensorTags()

            # Connect the TI sensor tags
            tag1 = SensorTag(addr1)
            tag2 = SensorTag(addr2)
            tag3 = SensorTag(addr3)
            
            # Turn on the tag accelerometers
            tags = [tag1, tag2, tag3]
            for tag in tags:
                tag.accelerometer.enable()

            connected = True
            okayStatus()

        if checkButton() and connected and not calibrated:
            clearAll()
            [leftTag, centerTag, rightTag] = orderTags(tag1, tag2, tag3)
            calibrated = True

        # Read accel data if connected
        if calibrated:
            try:
                leftAccl = leftTag.accelerometer.read()
                rightAccl = rightTag.accelerometer.read()
                centerAccl = centerTag.accelerometer.read()
                print 'LEFT_ACCL', leftAccl
                print 'RIGHT_ACCL', rightAccl
                print 'CENTER_ACCL', centerAccl

                # Calculate posture state (TODO)
                angle = calculateAngle(leftAccl, rightAccl)
                sleeping = calculateSleeping(centerAccl)
                print 'ANGLE', angle
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
                calibrated = False

        if not calibrated:
            if blinkToggle:
                setOkay()
            else:
                clearOkay()
            blinkToggle = not blinkToggle

        time.sleep(DEFAULT_SPIN_TIME)
