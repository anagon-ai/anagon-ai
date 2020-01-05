import logging

from core import Core
from modules.EchoBot.module import EchoBot
from modules.TimeBot.module import TimeBot
from modules.TextInput.module import TextInputModule

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

  ai = Core()
  ai.add_module(EchoBot())
  ai.add_module(TimeBot())
  # ai.add_module(KafkaProducer())
  ai.add_module(TextInputModule())

  ai.boot()
