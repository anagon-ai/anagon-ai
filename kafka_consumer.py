import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
  'random-topic-1234',
  bootstrap_servers='127.0.0.1:9092',
  auto_offset_reset='earliest',
  value_deserializer=json.loads
)

for msg in consumer:
  print(msg.value)
