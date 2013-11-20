import main
import time

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
    self.sleeping = sleeping
    self.angleBuffer.pop(0)
    self.angleBuffer.append(angle)

    self.socket.updateAngle(angle)

    newStabilized = abs(min(self.angleBuffer) - max(self.angleBuffer)) < 2*ANGLE_DEVIATION

    if not self.stabilized:
      if newStabilized:
        print "stabilized!"
        self.stabilized = True
        self.startTime = time.time() * 1000 - MIN_FOR_TURN * 60 * 1000
        self.logLastTurn()
    else:
      if newStabilized:
        delayTime = self.sleepIntervalMs
        if not self.sleeping:
          delayTime = self.sitIntervalMs
        if time.time() * 1000 - self.startTime > delayTime:
          self.late = True
          fireAlarm()
      else:
        self.saveLastTurn()
        self.stabilized = False
        self.late = False

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

  def fireAlarm(self):
    # TODO
    print "ALARM!"
    pass
