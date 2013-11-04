from Model import *

class ModuleModel(Model):
  def __init__(self, id):
    # Model defaults
    data = {
      "id": id,
      "angle": 0,
      "sleep_interval_ms": 7200000,
      "sit_interval_ms": 900000
    }

    Model.__init__(self, data)