from dataclasses import dataclass

from core.events import BaseEvent
from modules.BaseModule import BaseModule

# correct (extending BaseEvent):
@dataclass
class ExampleEvent(BaseEvent):
  text: str

# incorrect
@dataclass
class ExampleEvent:
  text: str

class ExampleModule(BaseModule):
  def boot(self):
    self.subscribe(self.handle, ExampleEvent)