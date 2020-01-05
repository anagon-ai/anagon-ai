from core import Core


class BaseModule:
  core: Core

  def boot(self, core: Core):
    self.core = core

  def handle(self, message):
    pass