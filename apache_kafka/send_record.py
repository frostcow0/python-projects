#!/usr/bin/env python

from uuid import uuid4
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from utils.parse_command_line_args import send_parse_command_line_args
from utils.schemas import DATA_SCHEMA, data_to_dict, Data


def send_record(args):
    """ Sends Record using a SerializingProducer & AvroSerializer """
    topic = args.topic.rstrip()

    schema_registry_config = {
        'url': args.schema_registry }
    schema_registry_client = SchemaRegistryClient(schema_registry_config)

    avro_serializer = AvroSerializer(
        schema_registry_client,
        DATA_SCHEMA,
        data_to_dict)

    producer_config = {
        "bootstrap.servers": args.bootstrap_servers,
        "key.serializer": StringSerializer('utf_8'),
        "value.serializer": avro_serializer
    }
    producer = SerializingProducer(producer_config)

    split_incoming_data = args.record_value.split(',')
    if not len(split_incoming_data) == 7: # Data Format Check
        print('** Error: Insufficient Incoming Data: ', split_incoming_data)
        raise Exception
    try: # Data Format Check
        incoming_data = {
            'envId': int(split_incoming_data[0]),
            'whenCollected': str(split_incoming_data[1]),
            'timeLightOnMins': int(split_incoming_data[2]),
            'humidity': int(split_incoming_data[3]),
            'soilMoisture': int(split_incoming_data[4]),
            'temperature': int(split_incoming_data[5]),
            'waterConsumption': int(split_incoming_data[6]) }
    except Exception as error:
        print('** Error Creating Dict of Data: ', error)

    print(f'Producing data records to topic {topic}. ^C to exit.')
    producer.poll(1)
    try:
        key = args.record_key if args.record_key else str(uuid4())
        data_object = Data(incoming_data)
        print('\t-Producing Avro record. . .')
        producer.produce(topic = topic,
                        key = key,
                        value = data_object,
                        on_delivery = delivery_report)
    except ValueError:
        print('\t-Invalid input, discarding record. . .')
    print('\nFlushing records. . .')
    producer.flush()

def delivery_report(err, msg):
    """ Handles Record Callback """
    if err is not None:
        print(f'\t-Failed to deliver message: {err}')
    else:
        print(f'\t-Produced record to topic {msg.topic()}, '
        f'partition {msg.partition()}, '
        f'@ offset {msg.offset()}')


if __name__ == "__main__":
    # print('Let\'s pretend that I\'ve produced :)')
    send_record(send_parse_command_line_args())
