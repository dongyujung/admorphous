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

# Kafka settings
bootstrap_server_list = ["10.0.0.9:9092"]
topic_name = "VIEWS_PAGE_WIN_FILTERED"

# Postgres settings
table = 'views_page'
db_host_ip = "10.0.0.5"
db_port = "5432"
db_type = "postgres"
usr = config.username
pwrd = config.password


try:
    # Kafka Consumer
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_server_list,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Connection to Postgres DB
    connection = psycopg2.connect(user=usr,
                                  password=pwrd,
                                  host=db_host_ip,
                                  port=db_port,
                                  database=db_type)
    cursor = connection.cursor()

    # Receiving and accumulating 20 messages at a time and inserting into db
    i = 0
    # append each row as set in rows list
    rows = []
    for message in consumer:

        i += 1
        inbound_dict = message.value

        # Row to be inserted
        row = (inbound_dict['DOCUMENT_ID'],
               inbound_dict['COUNT'],
               datetime.fromtimestamp(message.timestamp / 1e3),
               datetime.now(),
               inbound_dict['WIN_END'])
        print(row)
        rows.append(row)

        # Commit insert for every 20 messages received
        if i % 20 == 0:
            rows_template = ','.join(['%s'] * len(rows))
            insert_query = 'INSERT INTO views_page (document_id, count, produce_time, consume_time, window_end) ' \
                           'VALUES {};'.format(rows_template)
            cursor.execute(insert_query, rows)
            connection.commit()
            del rows
            rows = []


except Exception as e:
    print(e)
finally:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed \n")
