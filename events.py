from dataclasses import dataclass


@dataclass
class TextInput:
  type = 'be.anagon.ai.poc.text.input'
  text: str