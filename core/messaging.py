from dataclasses import dataclass
from uuid import UUID

from core.events import BaseEvent


@dataclass
class Metadata:
  id: UUID

@dataclass
class Message:
  event: BaseEvent
  metadata: Metadata
