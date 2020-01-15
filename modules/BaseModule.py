from typing import Callable, List, Type, Union

from core.types import AnyEventHandler
from core.errors import ModuleError
from core.events import BaseEvent
from core.messaging import Metadata
from util.developer_help import message_with_example


class BaseModule:
  def attach(self, publish: Callable, subscribe: Callable) -> None:
    # override publish and subscribe without losing IDE assistance
    setattr(self, 'publish', publish)
    setattr(self, 'subscribe', subscribe)
    pass

  def publish(self, event: BaseEvent, metadata: Metadata = None) -> None:
    raise ModuleError(message_with_example(
      example="docs/examples/append_module.py",
      message="""
    %(class)s was not attached to Core before publishing.

    You cannot boot your module directly (like: %(class)s.boot()).
    It must instead be added to the AI Core, which is boots the modules for you. 

    """ % {'class': self.__class__.__name__}
      ))

  def subscribe(self, handler: AnyEventHandler,
                types: Union[List[Type[BaseEvent]], Type[BaseEvent]] = None) -> None:
    raise ModuleError(message_with_example(
      example="docs/examples/append_module.py",
      message="""
%(class)s was not attached to Core before subscribing.

You cannot boot your module directly (like: %(class)s.boot()).
It must instead be added to the AI Core, which is boots the modules for you. 

""" % {'class': self.__class__.__name__}
      ))

  def boot(self) -> None:
    raise NotImplementedError(message_with_example(
      example="docs/examples/module_implement_boot.py",
      params={'ExampleClass': self.__class__.__name__},
      message="""
ExampleClass should override the parent boot() method.
- Either `def booth()` is missing
- Or `def boot()` is calling the parent method: super().boot().

Add a boot() method and subscribe to events.
""", object=self))
