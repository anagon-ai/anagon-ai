import threading
from time import sleep

from core import Core
from modules.BaseModule import BaseModule
from events import TextInput


class TextInputModule(BaseModule):

  def boot(self, core: Core):
    super().boot(core)

    def input_loop():
      sleep(0.1)
      while True:
        text = input("Input: ")
        core.publish(TextInput(text=text))

    threading.Thread(target=input_loop).start()

  def handle(self, message):
    pass
