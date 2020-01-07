from core.events import TextInput, TextOutput
from modules.BaseModule import BaseModule


class EchoBot(BaseModule):

  def boot(self):
    self.subscribe(handler=self.handle, types=TextInput)

  def handle(self, message: TextInput):
    self.publish(TextOutput(text="You wrote: %s" % message.text))
