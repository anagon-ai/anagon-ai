import datetime
from collections import namedtuple


class Core:
  def __init__(self):
    self.modules = []

  def add_module(self, module):
    self.modules.append(module)

  def boot(self):
    for module in self.modules:
      module.boot(self)

  def publish(self, message):
    for module in self.modules:
      module.handle(message)


TextInput = namedtuple('TextInput', ['text'])


class TextInputModule:

  def boot(self, core: Core):
    while True:
      text = input("Input: ")
      core.publish(TextInput(text=text))

  def handle(self, message):
    pass


class TextInputDisplayModule:
  def boot(self, core: Core):
    pass

  def handle(self, message):
    print("You wrote: %s" % message.text)


class BaseModule:
  def boot(self, core: Core):
    self.core = core


class TimeBot(BaseModule):
  def handle(self, message: TextInput):
    if message.text.find('time') > -1:
      print('The time is: %s' % datetime.datetime.now().strftime('%H:%M:%S'))


if __name__ == '__main__':
  ai = Core()
  ai.add_module(TextInputModule())
  ai.add_module(TextInputDisplayModule())
  ai.add_module(TimeBot())

  ai.boot()