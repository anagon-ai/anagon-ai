import logging
from collections import defaultdict
from typing import List


class Core:
  modules: List
  handlers: List = defaultdict(list)

  def __init__(self):
    self.modules = []
    self.booted = False

  def add_module(self, module):
    logging.info("Registering: %s" % type(module).__name__)
    self.modules.append(module)

  def boot(self):
    for module in self.modules:
      logging.info("Booting module: %s" % type(module).__name__)

      module.core = self
      module.boot()

    self.booted = True
    logging.info("Booted all modules")

  def publish(self, message):
    if not self.booted:
      raise CoreException("AI has not been booted yet. Please run Core.boot() before publishing.")

    for handler in self.handlers[message.type]:
      handler(message)

    for handler in self.handlers[None]:
      handler(message)

  def subscribe(self, handler, types=None):
    # todo: permission check
    if type(types) != list:
      types = [types]

    for _type in types:
      self.handlers[_type].append(handler)


class CoreException(Exception):
  pass
