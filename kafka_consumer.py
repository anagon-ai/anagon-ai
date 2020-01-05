import json
import logging

from kafka import KafkaConsumer

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO, datefmt='%H:%M:%S')

consumer = KafkaConsumer(
  # pattern = '.*',
  #group_id='second',
  bootstrap_servers='127.0.0.1:9092',
  auto_offset_reset='earliest',
  # value_deserializer=json.loads
)

consumer.subscribe(pattern='.*')
for msg in consumer:
  print(msg.value)
