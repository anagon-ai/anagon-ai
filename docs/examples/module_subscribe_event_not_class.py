from core.events import TextInput
from modules.BaseModule import BaseModule


class ExampleModule(BaseModule):

  def boot(self):
    # correct
    self.subscribe(self.handle)
    self.subscribe(self.handle, TextInput)
    self.subscribe(self.handle, [TextInput])

    # incorrect
    self.subscribe(self.handle, 'EventAsString')

  def handle(self):
    pass
