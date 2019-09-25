"""
Converts csv file to a stream of JSON, sends to Kafka topic.
Input arguments: script, input csv path, topic name, bootstrap servers
"""
# Import packages
import sys
import csv
import json
from time import sleep
from kafka import KafkaProducer

# Shell script input arguments
args = sys.argv

# There should be four or more input arguments:
# script, input csv path, topic name, bootstrap servers
if len(args) >= 4:
    input_file_path = args[1]
    topic_name = args[2]
    bootstrap_server_list = args[3:]
else:
    raise Exception('Need at least four input arguments.')

# Set up Kafka Producer
producer = KafkaProducer(bootstrap_servers=bootstrap_server_list,
                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))

# Send JSON stream to topic
with open(input_file_path, 'r', encoding='utf-8') as file:
    # Csv reader iterator
    file_reader = csv.DictReader(file)

    for row in file_reader:
        n = file_reader.line_num - 1   # Starts at 1
        if n > 100:
            break

        producer.send(topic_name, value=row)
        sleep(1)


