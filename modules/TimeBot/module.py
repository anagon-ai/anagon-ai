import datetime

from modules.BaseModule import BaseModule
from events import TextInput


class TimeBot(BaseModule):

  def boot(self):
    super().boot()
    self.core.subscribe(handler=self.handle, types=TextInput.type)

  def handle(self, message: TextInput):
    if message.text.find('time') > -1:
      print('The time is: %s' % datetime.datetime.now().strftime('%H:%M:%S'), flush=True)