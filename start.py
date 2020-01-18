import logging

from core.core import Core
from modules.CommandHelper.module import CommandHelper
from modules.EchoBot.module import EchoBot
from modules.EventLoggingBot.module import EventLoggingBot
from modules.ReminderBot.module import ReminderBot
from modules.TimeBot.module import TimeBot
from modules.ConsoleModule.module import ConsoleModule

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

  ai = Core()
  ai.add_module(EchoBot())
  ai.add_module(TimeBot())
  ai.add_module(EventLoggingBot('ai.log'))
  ai.add_module(ReminderBot())
  ai.add_module(ConsoleModule())
  ai.add_module(CommandHelper())

  ai.boot()
