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
        print "USB stick found."
    except IndexError:
        print "No USB stick found."
        storage_prefix = None

    # Create the state controller
    state = ModuleStateController(LOCAL_PREFIX, storage_prefix)

    # Connection loop variables
    connected = False
    calibrated = False
    blinkToggle = False

    # Begin operating loop
    print "Waiting for button press to find tags."
    while True:
        # Check if the user has pushed the sync button.
        # If so and we have not connected yet, do the connection
        if checkButton() and not connected and not calibrated:
            print "Connecting tags..."
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
            print "Tags connected."
            print "Waiting for button press to determine tag locations."
            print "Please apply tags to patient."

        # Now that we've found the tags, figure out which is on what part
        # Wait for user input to ensure tags are on patient
        if checkButton() and connected and not calibrated:
            print "Locating tags..."
            clearAll()
            [leftTag, centerTag, rightTag] = orderTags(tag1, tag2, tag3)
            calibrated = True
            setOkay()
            print "Tags located."
            print "Beginning monitoring loop:"

        # Read accel data if connected and locations identified
        if calibrated:
            try:
                leftAccl = leftTag.accelerometer.read()
                rightAccl = rightTag.accelerometer.read()
                centerAccl = centerTag.accelerometer.read()

                # Calculate posture state
                angle = calculateAngle(leftAccl, rightAccl)
                sleeping = calculateSleeping(centerAccl)
                print 'Body Angle', angle
                print 'Sleeping?', sleeping

                # Pass to state controller that will handle the rest
                state.updateState(angle, sleeping)

                # Wait to take the next reading
                time.sleep(SEC_PER_READING - DEFAULT_SPIN_TIME)

            # In case the sensor tags disconnect/fail
            except btle.BTLEException:
                clearAll()
                errorStatus()
                triggerAlarm()

                connected = False
                calibrated = False

        # Flash this light to let user know they need to push the button
        if not calibrated:
            if blinkToggle:
                setOkay()
            else:
                clearOkay()
            blinkToggle = not blinkToggle

        # Default wait between each loop (checking for button or reading)
        time.sleep(DEFAULT_SPIN_TIME)
