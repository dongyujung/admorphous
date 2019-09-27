"""
Load data from topic into PostgreSQL database.
Input arguments: script, table name, topic name, bootstrap servers
"""
# Packages
import sys
from kafka import KafkaConsumer
import psycopg2
import json
import config
import datetime


topic_name = "platform"
table = 'test'
query = "INSERT INTO test ('platform', 'count', 'created_on') VALUES (?, ?, ?)"
bootstrap_server_list = ["10.0.0.9:9092"]
usr = config.username
pwrd = config.password


connection = psycopg2.connect(user=usr,
                              password=pwrd,
                              host="10.0.0.5",
                              port="5432",
                              database="postgres")


cursor = connection.cursor()

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_server_list,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:

    inbound_dict = message.value
    print(inbound_dict)
    cursor.execute(query, (inbound_dict['platform'], inbound_dict['count'],
                                datetime.now(timezone.utc)))



if (connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed \n")