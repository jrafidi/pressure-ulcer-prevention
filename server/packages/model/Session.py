from Model import *

class Session():
  def __init__(self):
    self.moduleModels = {}

    self.moduleIdList = Model({"ids": []})

    self.megaBinds = {}

  def bindAllModules(self, event, callback):
    self.megaBinds[event] = callback
    for id, module in self.moduleModels.iteritems():
      module.on(event, callback)

  def addModule(self, module):
    id = module.get("id")
    self.moduleModels[id] = module

    idList = list(self.moduleIdList.get("ids"))
    idList.append(id)
    self.moduleIdList.set("ids", idList)

    for event, callback in self.megaBinds.iteritems():
      module.on(event, callback)

  def removeModule(self, id):
    del self.moduleModels[id]
    idList = list(self.moduleIdList.get("ids"))

    if id in idList:
      idList.remove(id)
      self.moduleIdList.set("ids", idList)