from typing import Callable, Coroutine, Optional

from core.errors import ModuleAddedTaskBeforeAttachingError, ModulePublishedBeforeAttachingError, \
  ModuleSubscribedBeforeAttachingError
from core.events import All, BaseEvent
from core.messaging import Metadata
from core.types import AnyEventHandler, EventTypes
from util.developer_help import message_with_example


class BaseModule:
  def attach(self, publish: Optional[Callable] = None, subscribe: Optional[Callable] = None,
             add_task: Optional[Callable] = None) -> None:
    # override publish and subscribe without losing IDE assistance
    if publish:
      setattr(self, 'publish', publish)
    if subscribe:
      setattr(self, 'subscribe', subscribe)
    if add_task:
      setattr(self, 'add_task', add_task)

  def publish(self, event: BaseEvent, metadata: Metadata = None) -> None:
    raise ModulePublishedBeforeAttachingError(module=self)

  def subscribe(self, handler: AnyEventHandler, types: EventTypes = All) -> None:
    raise ModuleSubscribedBeforeAttachingError(module=self)

  def add_task(self, task: Coroutine) -> None:
    raise ModuleAddedTaskBeforeAttachingError(module=self)

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
