"""
Includes function that converts display csv file to a stream of JSON, sends to Kafka topic.
Called by events_to_topic.py whenever a dump of display_ad mapping is needed.
"""
# Import packages
import csv
import json
import itertools
from datetime import datetime
from kafka import KafkaProducer


def send_mapping(bootstrap_server_list,
                 display_file_path,
                 start_line,
                 start_display_id,
                 dump_size):
    """
    Sets up Kafka producer and sends each line of the csv file to the Kafka topic as JSON.

    Args:
        bootstrap_server_list (list): List of Kafka server IP addresses and port, e.g., 'localhost:9092'.
        display_file_path (str): Display csv file path.
        start_line (str): Which line to start csv reading.
        start_display_id(str): display_id to start csv reading.
        dump_size (int): Dump size of display-ad mappings.

    Returns:
        line_number (int): Line number before which where the current reading ended.
        line_display_id (str): display_id before which the current reading ended.

    """
    last_display_id = start_display_id + dump_size -1

    # Set up Kafka Producer
    producer = KafkaProducer(bootstrap_servers=bootstrap_server_list,
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))

    # Send JSON stream to topic with no sleep time
    with open(display_file_path, 'r', encoding='utf-8') as file:
        # Csv reader iterator
        file_reader = csv.DictReader(file)

        for row in itertools.islice(file_reader, start_line, None):
            # Start iteration at Nth line
            # Stop iteration if display_id higher than expected
            # and send line number back to events producer
            # for reference in next batch
            line_display_id = int(row['display_id'])
            if line_display_id > last_display_id:
                line_number = file_reader.line_num
                return line_number, line_display_id

            # Set timestamp
            row['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print(row)

            # Send JSON to Kafka topic
            producer.send('display_ad', value=row)


