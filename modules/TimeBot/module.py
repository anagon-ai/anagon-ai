import datetime

from core.events import TextInput, TextOutput
from modules.BaseModule import BaseModule


class TimeBot(BaseModule):

  def boot(self) -> None:
    self.subscribe(handler=self.handle, types=TextInput)

  def handle(self, event: TextInput) -> None:
    if event.text.find('time') > -1:
      self.publish(TextOutput(text='The time is: %s' % datetime.datetime.now().strftime('%H:%M:%S')))
