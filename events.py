from dataclasses import dataclass


@dataclass
class TextInput:
  type = 'be.anagon.ai.poc.text.input'
  text: str


@dataclass
class TextOutput:
  type = 'be.anagon.ai.poc.text.output'
  text: str