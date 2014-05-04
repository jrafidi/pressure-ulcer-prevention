import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

RELAY_PIN = 18
ERROR_PIN = 17
ALARM_PIN = 21
OKAY_PIN = 22
BUTTON_PIN = 23

# Active low
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)

# LEDs
GPIO.setup(ERROR_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ALARM_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(OKAY_PIN, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(BUTTON_PIN, GPIO.IN)

def triggerAlarm():
  GPIO.output(ALARM_PIN, GPIO.HIGH)
  GPIO.output(RELAY_PIN, GPIO.LOW)

def untriggerAlarm():
  GPIO.output(ALARM_PIN, GPIO.LOW)
  GPIO.output(RELAY_PIN, GPIO.HIGH)

def okayStatus():
  GPIO.output(ERROR_PIN, GPIO.LOW)
  GPIO.output(OKAY_PIN, GPIO.HIGH)

def errorStatus():
  GPIO.output(ERROR_PIN, GPIO.HIGH)
  GPIO.output(OKAY_PIN, GPIO.LOW)

def clearAll():
  GPIO.output(OKAY_PIN, GPIO.LOW)
  GPIO.output(ALARM_PIN, GPIO.LOW)
  GPIO.output(ERROR_PIN, GPIO.LOW)
  GPIO.output(RELAY_PIN, GPIO.HIGH)

def checkButton():
  return GPIO.input(BUTTON_PIN)