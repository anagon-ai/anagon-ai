from core import Core


class BaseModule:
  core: Core

  def boot(self):
    pass

  def handle(self, message):
    pass
