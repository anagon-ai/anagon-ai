from kafka import KafkaProducer
import uuid
import json

producer = KafkaProducer(
    bootstrap_servers=['127.0.0.1:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for _ in range(10):
    producer.send('random-topic-1234', {"id": str(uuid.uuid4())})
    producer.flush()