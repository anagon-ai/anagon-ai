from dataclasses import dataclass

@dataclass
class BaseEvent:
  @property
  def type(self):
    raise NotImplementedError

  @property
  def as_dict(self):
    event_dict = {**self.__dict__}
    for attr in dir(self):
      if not attr.startswith('__') and attr != 'as_dict':
        event_dict[attr] = getattr(self, attr)
    return event_dict


@dataclass
class TextInput(BaseEvent):
  type = 'be.anagon.ai.poc.text.input'
  text: str


@dataclass
class TextOutput(BaseEvent):
  type = 'be.anagon.ai.poc.text.output'
  text: str
