# Packages
import sys
from kafka import KafkaConsumer
import json


# Kafka settings
bootstrap_server_list = ["10.0.0.9:9092"]
topic_name = "pageviews"


consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_server_list,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='simple',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:

    #inbound_dict = message.value
    #headers = message.headers


    print(message)


