import logging

from modules.BaseModule import BaseModule


class EchoBot(BaseModule):
  def handle(self, message):
    logging.info("You wrote: %s" % message.text)