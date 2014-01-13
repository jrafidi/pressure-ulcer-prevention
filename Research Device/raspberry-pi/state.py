import main
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, True)

ANGLE_DEVIATION = 5
MIN_FOR_TURN = 2

BUFFER_SIZE = MIN_FOR_TURN * 60

DEF_SLEEP_INTERVAL = 7200000
DEF_SIT_INTERVAL = 900000

class ModuleStateController():
  def __init__(self):
    # Current measuring vars
    self.sleeping = True
    self.stabilized = False
    self.late = False
    self.angleBuffer = [1000] * BUFFER_SIZE
    self.startTime = time.time() * 1000
    self.lastTurn = None

    # Setting vars
    self.sleepIntervalMs = DEF_SLEEP_INTERVAL
    self.sitIntervalMs = DEF_SIT_INTERVAL

  def setSocketFactory(self, socketFactory):
    self.socket = socketFactory

  def updateState(self, angle, sleeping):
    # Update sleeping state
    self.sleeping = sleeping

    # Update angle buffer
    self.angleBuffer.pop(0)
    self.angleBuffer.append(angle)

    # Let the socket know the angle has changed
    self.socket.updateState(angle, sleeping)

    # Check if the angles in the buffer fall in the desired range
    newStabilized = abs(min(self.angleBuffer) - max(self.angleBuffer)) < 2*ANGLE_DEVIATION

    # If we were unstable before:
    if not self.stabilized:
      # and we are now stable:
      if newStabilized:
        print "Stabilized"
        # Set ourselves to be stable
        self.stabilized = True

        # If this is our first time stabilizing, set the start time
        # and finish
        if self.lastTurn == None:
          self.startTime = time.time()*1000 - MIN_FOR_TURN * 60 * 1000
          return

        # If we have deviated away from the previous turn's angle,
        # log the turn and reset the start time for the next one
        if min(self.angleBuffer) > self.lastTurn['angle'] or\
           max(self.angleBuffer) < self.lastTurn['angle']:
          self.startTime = time.time() * 1000 - MIN_FOR_TURN * 60 * 1000
          self.logLastTurn()

    # If we were stable before:
    else:
      # and we are still stable:
      if newStabilized:
        # Determine whether or not we need to fire the alarm
        delayTime = self.sleepIntervalMs
        if not self.sleeping:
          delayTime = self.sitIntervalMs
        if time.time() * 1000 - self.startTime > delayTime:
          # If we already flagged as late, then no point in firing again
          if not self.late:
            self.late = True
            self.fireAlarm()

      # If we are not stable anymore
      else:
        # Save off this turn and clear stable/late flags
        print "Destabilized"
        self.saveLastTurn()
        self.stabilized = False
        self.late = False
        self.unfireAlarm()

  def logLastTurn(self):
    if self.lastTurn != None:
      self.socket.logTurn(self.lastTurn)

  def saveLastTurn(self):
    self.lastTurn = {
      'deviceId': main.MODULE_ID,
      'angle': self.angleBuffer[0],
      'sleeping': self.sleeping,
      'startTime': self.startTime,
      'endTime': time.time() * 1000,
      'late': self.late
    }

  def debug(self, vals):
    self.socket.debug(vals)

  def fireAlarm(self):
    GPIO.output(10, False)

  def unfireAlarm(self):
    GPIO.output(10, True)
