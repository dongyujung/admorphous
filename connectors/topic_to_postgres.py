"""
Load data from topic into PostgreSQL database.
Input arguments: script, table name, topic name, bootstrap servers
"""
# Packages
import sys
from kafka import KafkaConsumer
from json

# Shell script input arguments
args = sys.argv

# There should be four or more input arguments:
# script, table name, topic name, bootstrap servers
if len(args) >= 4:
    table_name = args[1]
    topic_name = args[2]
    bootstrap_server_list = args[3:]
else:
    raise Exception('Need at least four input arguments.')

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_server_list,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:

    print(message)