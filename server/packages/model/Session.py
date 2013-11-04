class Session():
  def __init__(self):
    self.moduleModels = {}

  def bindAllModules(self, event, callback):
    for key, value in self.moduleModels.iterItems:
      value.on(event, callback)