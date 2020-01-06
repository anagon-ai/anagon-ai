import logging

from events import TextInput
from modules.BaseModule import BaseModule


class EchoBot(BaseModule):

  def boot(self):
    super().boot()
    self.core.subscribe(types=TextInput.type, handler=self.handle)

  def handle(self, message: TextInput):
    logging.info("You wrote: %s" % message.text)