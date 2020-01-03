import datetime
import json
import logging
import kafka
from dataclasses import dataclass


class Core:
  def __init__(self):
    self.modules = []

  def add_module(self, module):
    logging.info("Registering: %s" % type(module).__name__)
    self.modules.append(module)

  def boot(self):
    for module in self.modules:
      logging.info("Booting module: %s" % type(module).__name__)

      module.boot(self)

    logging.info("Booted all modules")

  def publish(self, message):
    for module in self.modules:
      module.handle(message)


@dataclass
class TextInput:
  type = 'be.anagon.ai.poc.text.input'
  text: str


class BaseModule:
  core: Core

  def boot(self, core: Core):
    self.core = core

  def handle(self, message):
    pass


class TextInputModule(BaseModule):

  def boot(self, core: Core):
    super().boot(core)
    while True:
      text = input("Input: ")
      core.publish(TextInput(text=text))

  def handle(self, message):
    pass


class TextInputDisplayModule(BaseModule):
  def handle(self, message):
    logging.info("You wrote: %s" % message.text)


class TimeBot(BaseModule):
  def handle(self, message: TextInput):
    if message.text.find('time') > -1:
      print('The time is: %s' % datetime.datetime.now().strftime('%H:%M:%S'), flush=True)


class HelloWorld(BaseModule):
  def boot(self, core: Core):
    super().boot(core)
    print("Modular AI started", flush=True)


class KafkaProducer(BaseModule):
  producer: kafka.KafkaProducer

  def boot(self, core: Core):
    self.producer = kafka.KafkaProducer(
      value_serializer=lambda v: json.dumps(v.__dict__).encode('utf-8')
    )

  def handle(self, message):
    self.producer.send(message.type, message)


if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

  ai = Core()
  ai.add_module(TextInputDisplayModule())
  ai.add_module(TimeBot())
  ai.add_module(HelloWorld())
  ai.add_module(KafkaProducer())
  ai.add_module(TextInputModule())

  ai.boot()
