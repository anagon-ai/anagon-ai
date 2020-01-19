from abc import ABCMeta
from dataclasses import dataclass
from typing import Any, Dict, List

from typing_extensions import TypedDict

BaseEventDict = TypedDict('BaseEventDict', {'type': str}, total=False)


@dataclass
class BaseEvent:
  @property
  def type(self) -> str:
    raise NotImplementedError

  @property
  def __static_attributes__(self) -> Dict[str, Any]:
    return {
        attr: getattr(self, attr)
        for attr in dir(self)
        if not attr.startswith('_') and attr not in ['dict'] and attr not in self.__dict__
        }

  def __getstate__(self) -> Dict[str, Any]:
    state = self.__dict__.copy()
    state.update(self.__static_attributes__)
    return state

  @property
  def dict(self) -> Dict[str, Any]:
    return self.__getstate__()

class All(BaseEvent, metaclass=ABCMeta):
  pass

@dataclass
class TextInput(BaseEvent):
  type = 'be.anagon.ai.poc.text.input'
  text: str


@dataclass
class TextOutput(BaseEvent):
  type = 'be.anagon.ai.poc.text.output'
  text: str

@dataclass
class TextCommand(BaseEvent):
  type = 'be.anagon.ai.poc.text.command'
  command: str
  args: List[str]

class ExitCommand(BaseEvent):
  type = 'be.anagon.ai.poc.command.exit'

@dataclass
class TextCommandInfo(BaseEvent):
  type = 'be.anagon.ai.poc.text.command.info'
  command: str
  description: str