from dataclasses import dataclass
from typing import Dict
from uuid import UUID

from dataclasses_json import dataclass_json
from typing_extensions import TypedDict

from core.events import BaseEvent, BaseEventDict


class MetadataDict(TypedDict, total=True):
  event: BaseEventDict
  metadata: Dict

@dataclass_json
@dataclass
class Metadata:
  id: UUID

@dataclass
class Message:
  event: BaseEvent
  metadata: Metadata
