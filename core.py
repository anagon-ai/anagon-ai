import logging
from collections import defaultdict
from typing import List, Union

from events import BaseEvent
from lib.errors import CoreNotBootedError, ModulePublishedBadEventError


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
      module.attach(
        lambda event: self.publish(event, module),
        lambda handler, types=None: self._subscribe(module, handler, types))
      module.boot()

    self.booted = True
    logging.info("Booted all modules")

  def publish(self, event: BaseEvent, module=None):
    if not self.booted:
      raise CoreNotBootedError()

    if not isinstance(event, BaseEvent):
      raise ModulePublishedBadEventError(module=module, event=event)

    for handler in self.handlers[event.type]:
      handler(event)

    for handler in self.handlers[None]:
      handler(event)

  """Internal: Attaches a module's event handler to all types or a specific set of types"""

  def _subscribe(self, module, handler, types: Union[str, List[str], None] = None):
    # todo: permission check
    if type(types) != list:
      types = [types]

    for _type in types:
      self.handlers[_type].append(handler)
