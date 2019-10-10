"""
Converts events csv file to a stream of JSON, sends to Kafka topic.
Calls display_to_topic.py to also send display data every interval of time.
Input arguments: script, sleep time, bootstrap servers
"""
# Import packages
import sys
import csv
import json
from time import sleep
from datetime import datetime
from kafka import KafkaProducer
import display_to_topic as display
import os

# Shell script input arguments
args = sys.argv

# There should be four or more input arguments:
# script, sleep time, bootstrap servers
if len(args) >= 3:
    sleep_time = float(args[1])
    dump_size = int(args[2])
    bootstrap_server_list = args[3:]
else:
    raise Exception('Need at least four input arguments.')

events_file_path = os.path.join(os.path.expanduser('~'), 'admorphous', 'producers',
                                   'data', 'processed',
                                   'events.csv')
display_file_path = os.path.join(os.path.expanduser('~'), 'admorphous', 'producers',
                                   'data', 'processed',
                                   'display_ads.csv')
events_topic_name = 'events'


def send_events(bootstrap_server_list,
                events_file_path,
                display_file_path,
                topic_name,
                sleep_time,
                dump_size):
    """
    Sets up Kafka producer and sends each line of the csv file to the Kafka topic as JSON.

    Args:
        bootstrap_server_list (list): List of Kafka server IP addresses and port, e.g., 'localhost:9092'.
        events_file_path (str): Events csv file path.
        display_file_path (str): Display csv file path.
        topic_name (str): Name of Kafka topic that the data is sent to.
        sleep_time (float): Time interval between messages in seconds.
        dump_size (int): Dump size of display-ad mappings.

    Returns:

    """
    # Set up Kafka Producer
    producer = KafkaProducer(bootstrap_servers=bootstrap_server_list,
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))

    start_line, start_display_id = 1, 1
    # Send some mapping data initially
    line_number, line_display_id = display.send_mapping(bootstrap_server_list,
                                                        display_file_path,
                                                        start_line,
                                                        start_display_id,
                                                        dump_size)

    # Send JSON stream to topic
    with open(events_file_path, 'r', encoding='utf-8') as file:
        # Csv reader iterator
        file_reader = csv.DictReader(file)

        for i, row in enumerate(file_reader):

            if i % dump_size == 0:
                line_number, line_display_id = display.send_mapping(bootstrap_server_list, display_file_path,
                                                                    line_number,
                                                                    line_display_id, dump_size)
            # Set timestamp
            row['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print(row)

            # Send JSON to Kafka topic
            producer.send(topic_name, value=row)

            sleep(sleep_time)


if __name__ == "__main__":
    send_events(bootstrap_server_list,
                events_file_path,
                display_file_path,
                events_topic_name,
                sleep_time,
                dump_size)
