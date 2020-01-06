import json

import kafka

from core import Core
from modules.BaseModule import BaseModule


class KafkaProducer(BaseModule):
  producer: kafka.KafkaProducer

  def boot(self):
    self.producer = kafka.KafkaProducer(
      value_serializer=lambda v: json.dumps(v.__dict__).encode('utf-8')
    )
    self.core.subscribe(handler=self.handle)

  def handle(self, message):
    self.producer.send(message.type, message)