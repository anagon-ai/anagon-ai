from core.events import TextInput, TextOutput
from modules.BaseModule import BaseModule


class ExampleModule(BaseModule):

  def handle(self, event: TextInput):

    if event.text.startswith('!help'):
      # incorrect
      self.publish("Help message")

      # correct
      self.publish(TextOutput("Help message"))