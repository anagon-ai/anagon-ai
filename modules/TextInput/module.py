import threading
from time import sleep

from core import Core
from modules.BaseModule import BaseModule
from events import TextInput


class TextInputModule(BaseModule):

  def boot(self):

    def input_loop():
      sleep(0.1)
      while True:
        text = input("Input: ")
        self.core.publish(TextInput(text=text))

    threading.Thread(target=input_loop).start()