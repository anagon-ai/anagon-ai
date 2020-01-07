import datetime

from modules.BaseModule import BaseModule
from core.events import TextInput, TextOutput


class TimeBot(BaseModule):

  def boot(self):
    self.subscribe(handler=self.handle, types=TextInput.type)

  def handle(self, message: TextInput):
    if message.text.find('time') > -1:
      self.publish(TextOutput(text='The time is: %s' % datetime.datetime.now().strftime('%H:%M:%S')))