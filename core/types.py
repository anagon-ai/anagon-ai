from typing import Any, Union, List, Type

from typing_extensions import Protocol, runtime_checkable

from core.events import BaseEvent
from core.messaging import Metadata


class EventHandler(Protocol):
  def __call__(self, event: Any) -> None:
    pass


@runtime_checkable
class EventMetadataHandler(Protocol):
  def __call__(self, event: Any, metadata: Metadata) -> None:
    pass


class MetadataHandler(Protocol):
  def __call__(self, metadata: Metadata) -> None:
    pass


AnyEventHandler = Union[EventHandler, EventMetadataHandler, MetadataHandler]
Types = Union[Type[BaseEvent], List[Type[BaseEvent]], None]
