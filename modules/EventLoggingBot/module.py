import typing

from core.events import BaseEvent
from modules.BaseModule import BaseModule


class EventLoggingBot(BaseModule):
  file: typing.TextIO = None

  def __init__(self, log_location: str):
    self.log_location = log_location

  def boot(self):
    self.file = open(self.log_location, 'a')
    self.subscribe(self.handler)

  def handler(self, event: BaseEvent):
    self.file.write("Event received: %s\n" % (event,))
    self.file.flush()
