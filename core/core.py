import logging
from collections import defaultdict
from inspect import isclass
from typing import List, Union

from core.events import BaseEvent
from core.errors import CoreNotBootedError, ModulePublishedBadEventError, ModuleSubscribedToNonClassError, \
  ModuleSubscribedToNonEventClassError


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

  def _subscribe(self, module, handler, types: Union[str, BaseEvent, List[str], List[BaseEvent], None] = None):
    """Internal: Attaches a module's event handler to all types or a specific set of types"""

    # todo: permission check
    if module:
      pass

    if type(types) != list:
      types = [types]

    for _type in types:
      if isclass(_type):
        if issubclass(_type, BaseEvent):
          _type = _type.type
        else:
          raise ModuleSubscribedToNonEventClassError(event=_type, module=module)
      elif _type != None:
        raise ModuleSubscribedToNonClassError(event=_type, module=module)
      self.handlers[_type].append(handler)
