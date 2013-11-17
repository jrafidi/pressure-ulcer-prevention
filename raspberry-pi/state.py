import time

ANGLE_DEVIATION = 5
MIN_FOR_TURN = 2

DEF_SLEEP_INTERVAL = 7200000
DEF_SIT_INTERVAL = 900000

class ModuleStateController():
  def __init__(self):
    # Current measuring vars
    self.sleeping = True
    self.stabilized = False
    self.late = False
    self.startAngle = 0
    self.startTime = time.time() * 1000

    # Setting vars
    self.sleepIntervalMs = DEF_SLEEP_INTERVAL
    self.sitIntervalMs = DEF_SIT_INTERVAL

  def setSocketFactory(self, socketFactory):
    self.socket = socketFactory

  def updateState(self, angle, sleeping):
    self.sleeping = sleeping
    self.socket.updateAngle(angle)

    angleInRange = angle < self.startAngle + ANGLE_DEVIATION or angle > self.startAngle - ANGLE_DEVIATION
    stabilizeTimeElapsed = time.time()*1000 - self.startTime > MIN_FOR_TURN * 60 * 1000

    if (not self.stabilized) and stabilizeTimeElapsed:
      self.stabilized = True
      self.late = False
      self.startAngle = angle
      self.startTime = time.time()*1000

    if self.stabilized and angleInRange:
      delayTime = self.sleepIntervalMs
      if not self.sleeping:
        delayTime = self.sitIntervalMs
      if time.time() * 1000 - self.startTime > delayTime:
        self.late = True
        fireAlarm()

    if self.stabilized and (not angleInRange):
      self.stabilized = False
      self.logTurn()

  def logTurn(self):
    turnData = {
      deviceId: MODULE_ID
      angle: self.startAngle,
      sleeping: self.sleeping,
      startTime: self.startTime,
      endTime: time.time() * 1000
      late: self.late
    }

    self.socket.logTurn(turnData)

  def fireAlarm(self):
    # TODO
    pass