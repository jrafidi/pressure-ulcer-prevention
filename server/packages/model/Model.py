class Model():
  def __init__(self, initial_data):
    self.attributes = initial_data
    self.listeners = {}

  def set(self, attr, value):
    if self.attributes[attr] != value:
      self.attributes[attr] = value
      self.trigger("change", attr)
      self.trigger("change:" + attr, attr)

  def get(self, attr):
    return self.attributes[attr]

  def reset(self, data):
    self.attributes = data
    self.trigger("reset", data)

  def trigger(self, event, data):
    if event in self.listeners:
      for listener in self.listeners[event]:
        listener(self, data)

  def on(self, events, callback):
    eventItems = events.split(' ')
    for event in eventItems:
      if event in self.listeners:
        self.listeners[event].append(callback)
      else:
        self.listeners[event] = [callback]