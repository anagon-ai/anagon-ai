import logging

from core.core import Core
from modules.ConsoleModule.module import ConsoleModule
from modules.SignalRConnector.module import SignalRConnector
from modules.TimeBot.module import TimeBot

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

  ai = Core()
  ai.add_module(SignalRConnector('ws://localhost:5002/bothub'))
  ai.add_module(ConsoleModule())
  ai.add_module(TimeBot())

  ai.boot()
