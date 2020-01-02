import datetime
import json
import logging
import threading
from dataclasses import dataclass

from kafka import KafkaProducer, KafkaConsumer


class Core:
  def __init__(self, kafka_producer: KafkaProducer):
    self.modules = []
    self.kafka_producer = kafka_producer

  def add_module(self, module):
    logging.info("Registering: %s" % type(module).__name__)
    self.modules.append(module)

  def boot(self):
    threads = []
    for module in self.modules:
      logging.info("Booting module: %s" % type(module).__name__)

      def module_runner():
        module.boot(self)

        module_consumer = KafkaConsumer(
          TextInput.type,
          bootstrap_servers='127.0.0.1:9092',  # todo extract kafka config
          auto_offset_reset='earliest',
          value_deserializer=json.loads
        )

        for message in module_consumer:
          module.handle(message)

      module_thread = threading.Thread(target=module_runner, daemon=True)
      module_thread.start()
      threads.append(module_thread)

    logging.info("Booted all modules")

    for thread in threads:
      thread.join()

    logging.info("Shutting down")

  def publish(self, message):
    self.kafka_producer.send(message.type, message.__dict__)


@dataclass
class TextInput:
  type = 'be.anagon.ai.poc.text.input'
  text: str


class BaseModule:
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


if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

  producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
  )
  ai = Core(producer)
  ai.add_module(TextInputModule())
  ai.add_module(TextInputDisplayModule())
  ai.add_module(TimeBot())
  ai.add_module(HelloWorld())

  ai.boot()
