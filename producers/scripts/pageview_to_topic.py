"""
Converts pageviews csv file to a stream of JSON, sends to Kafka topic.
Input arguments: script, input csv path, topic name, bootstrap servers
"""
# Import packages
import sys
import csv
import json
from time import sleep
from datetime import datetime
from kafka import KafkaProducer
import os


# Shell script input arguments
args = sys.argv

# There should be four or more input arguments:
# script, sleep time, bootstrap servers
if len(args) >= 3:
    sleep_time = int(args[1])
    bootstrap_server_list = args[2:]
else:
    raise Exception('Need at least four input arguments.')

# Parameters
#bootstrap_server_list = ['localhost:9092']
pageviews_file_path = os.path.join(os.path.expanduser('~'), 'admorphous', 'producers',
                                   'data', 'processed',
                                   'page_views_sample_processed.csv')
pageviews_topic_name = 'pageviews'


def send_pageviews(
        bootstrap_server_list,
        input_file_path,
        topic_name,
        sleep_time
):
    """
    Sets up Kafka producer and sends each line of the csv file to the Kafka topic as JSON.

    Args:
        bootstrap_server_list (list): List of Kafka server IP addresses and port, e.g., 'localhost:9092'.
        input_file_path (str): Input csv file path.
        topic_name (str): Name of Kafka topic that the data is sent to.
        sleep_time (int): Time interval between messages in seconds.

    Returns:

    """
    # Set up Kafka Producer
    producer = KafkaProducer(bootstrap_servers=bootstrap_server_list,
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))

    # Send JSON stream to topic
    with open(input_file_path, 'r', encoding='utf-8') as file:
        # Csv reader iterator
        file_reader = csv.DictReader(file)

        for i, row in enumerate(file_reader):
            if i == 5000:
                break

            # Set timestamp
            row['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print(row)

            # Send message to topic
            producer.send(topic_name, value=row)

            sleep(sleep_time)


if __name__ == "__main__":
    send_pageviews(bootstrap_server_list, pageviews_file_path, pageviews_topic_name, sleep_time)