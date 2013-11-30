import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(10, GPIO.OUT)

while 1:
    time.sleep(1)
    print "ON"
    GPIO.output(10, False)
    time.sleep(1)
    print "OFF"
    GPIO.output(10, True)
