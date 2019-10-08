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
from datetime import datetime
from datetime import timezone

# Kafka settings
bootstrap_server_list = ["10.0.0.9:9092"]
topic_name = "IMPRESSIONS_AD_FILTERED"

# Postgres settings
table = 'impressions_ad'
db_host_ip = "10.0.0.5"
db_port = "5432"
db_type = "postgres"
usr = config.username
pwrd = config.password

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_server_list,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

query = "INSERT INTO impressions_ad (ad_id, count, created_on) VALUES (%s, %s, %s);"

connection = psycopg2.connect(user=usr,
                              password=pwrd,
                              host=db_host_ip,
                              port=db_port,
                              database=db_type)

cursor = connection.cursor()


for message in consumer:

    inbound_dict = message.value

    print(inbound_dict)
    cursor.execute(query, (inbound_dict['AD_ID'], inbound_dict['COUNT'],
                           datetime.now()))
    connection.commit()


if (connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed \n")