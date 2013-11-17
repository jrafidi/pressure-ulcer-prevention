from Model import *

class ModuleModel(Model):
  def __init__(self, id):
    # Model defaults
    data = {
      "deviceId": id,
      "angle": 0,
      "sleep_interval_ms": 7200000,
      "sit_interval_ms": 900000,
      "name": id,
      "notes": "",
      "turns": []
    }

    Model.__init__(self, data)