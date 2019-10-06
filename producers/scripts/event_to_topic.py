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
import display_to_topic as display

# Shell script input arguments
#args = sys.argv

# There should be four or more input arguments:
# script, input csv path, topic name, bootstrap servers
"""
if len(args) >= 4:
    input_file_path = args[1]
    topic_name = args[2]
    bootstrap_server_list = args[3:]
else:
    raise Exception('Need at least four input arguments.')
"""
input_file_path = '../data/processed/events.csv'

def send_events(bootstrap_server_list, sleep_time, dump_size):
    """

    :param bootstrap_server_list:
    :return:
    """

    # Set up Kafka Producer
    """
    producer = KafkaProducer(bootstrap_servers=bootstrap_server_list,
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))
                             """

    start_line, start_display_id = 1, 1
    line_number, line_display_id = display.send_mapping(bootstrap_server_list, start_line,
                                                        start_display_id, dump_size)

    # Send JSON stream to topic
    with open(input_file_path, 'r', encoding='utf-8') as file:
        # Csv reader iterator
        file_reader = csv.DictReader(file)

        for i, row in enumerate(file_reader):

            if i % dump_size == 0:
                line_number, line_display_id = display.send_mapping(bootstrap_server_list, line_number,
                                                                    line_display_id, dump_size)
                #input("Press Enter to continue...")

            if i == 1000:
                break

            print(i)
            print(row)

            #producer.send(topic_name, value=row)
            sleep(sleep_time)

send_events(1, 0.5, 10)
