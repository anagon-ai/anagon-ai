from dataclasses import dataclass

@dataclass
class BaseEvent:
  @property
  def type(self):
    raise NotImplementedError


@dataclass
class TextInput(BaseEvent):
  type = 'be.anagon.ai.poc.text.input'
  text: str


@dataclass
class TextOutput(BaseEvent):
  type = 'be.anagon.ai.poc.text.output'
  text: str
