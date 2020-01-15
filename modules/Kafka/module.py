import json

import kafka

from modules.BaseModule import BaseModule


class KafkaProducer(BaseModule):
  producer: kafka.KafkaProducer

  def boot(self):
    self.producer = kafka.KafkaProducer(
      value_serializer=lambda v: json.dumps(v.__dict__).encode('utf-8')
    )
    self.subscribe(self.handle)

  def handle(self, event):
    self.producer.send(event.type, event)