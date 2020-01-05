import logging


class Core:
  def __init__(self):
    self.modules = []

  def add_module(self, module):
    logging.info("Registering: %s" % type(module).__name__)
    self.modules.append(module)

  def boot(self):
    for module in self.modules:
      logging.info("Booting module: %s" % type(module).__name__)

      module.core = self
      module.boot(self)

    logging.info("Booted all modules")

  def publish(self, message):
    for module in self.modules:
      module.handle(message)


