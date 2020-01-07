from core.events import TextInput, TextOutput
from modules.BaseModule import BaseModule


class EchoBot(BaseModule):

  def boot(self):
    self.subscribe(types=TextInput.type, handler=self.handle)

  def handle(self, message: TextInput):
    self.publish(TextOutput(text="You wrote: %s" % message.text))
