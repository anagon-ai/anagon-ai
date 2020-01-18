from typing import Any, Union, List, Type, Coroutine, Optional

from typing_extensions import Protocol, runtime_checkable

from core.events import BaseEvent
from core.messaging import Metadata

@runtime_checkable
class EventHandler(Protocol):
  def __call__(self, event: Any) -> Optional[Coroutine]:
    pass


@runtime_checkable
class EventMetadataHandler(Protocol):
  def __call__(self, event: Any, metadata: Metadata) -> Optional[Coroutine]:
    pass

@runtime_checkable
class MetadataHandler(Protocol):
  def __call__(self, metadata: Metadata) -> Optional[Coroutine]:
    pass


AnyEventHandler = Union[EventHandler, EventMetadataHandler, MetadataHandler]
EventTypes = Union[Type[BaseEvent], List[Type[BaseEvent]]]
