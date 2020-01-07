import threading
from time import sleep

from core.events import TextInput, TextOutput
from modules.BaseModule import BaseModule


class CommandLineModule(BaseModule):

  def boot(self):
    def input_loop():
      sleep(0.1)
      while True:
        text = input("> ")
        self.publish(TextInput(text=text))

    threading.Thread(target=input_loop).start()

    self.subscribe(types=TextOutput.type, handler=self.output)

  def output(self, event: TextOutput):
    print(event.text)
