import typing

from core.events import BaseEvent, TextInput, TextOutput
from core.messaging import Metadata
from modules.BaseModule import BaseModule


class TemplateModule(BaseModule):
  example_field: str = None

  def boot(self):
    """ Initialize your module's fields and subscribe to relevant events. """

    self.example_field = 'foobar'

    self.subscribe(self.handler)                                  # subscribe to all
    self.subscribe(self.handle_text_input, TextInput)             # subscribe to TextInput only
    self.subscribe(self.handle_text_io, [TextInput, TextOutput])  # subscribe to two Event Types

  def handler(self, event: BaseEvent, metadata: Metadata):
    if isinstance(event, TextInput):
      event: TextInput
      print("TextInput with id %(id)s received: %(text)s" % dict(text=event.text, id=metadata.id))

  def handle_text_input(self, event: TextInput):
    self.publish(TextOutput("You said: %s" % event.text))

  def handle_text_io(self, event: typing.Union[TextInput, TextOutput]):
    print("Text input/output received: %s" % event.text)
