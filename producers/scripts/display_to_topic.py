"""
Converts display-ad mapping to a stream of JSON, sends to Kafka topic.
Sends batches of mapping when signaled from event stream.
...
"""
# Import packages
#import sys
import csv
import json
import itertools
#from time import sleep
from datetime import datetime
from kafka import KafkaProducer


def send_mapping(bootstrap_server_list, start_line,
                 start_display_id, dump_size):
    """

    :param start_line:
    :param start_display_id:
    :param bootstrap_server_list:
    :param current_display_id:
    :param dump_size:
    :return:
    line_number
    """
    last_display_id = start_display_id + dump_size -1
    input_file_path = '../data/processed/display_ad.csv'

    # Set up Kafka Producer
    """
    producer = KafkaProducer(bootstrap_servers=bootstrap_server_list,
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))
                             """


    # Send JSON stream to topic with no sleep time
    with open(input_file_path, 'r', encoding='utf-8') as file:
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

            row['timestamp'] = (datetime.now()- datetime.timedelta(seconds=3)).strftime('%Y-%m-%d %H:%M:%S')

            print(row)
            #producer.send('display_ad', value=row)


