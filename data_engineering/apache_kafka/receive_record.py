#!/usr/bin/env python

from confluent_kafka import DeserializingConsumer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

from utils.parse_command_line_args import receive_parse_command_line_args
from utils.schemas import DATA_SCHEMA, dict_to_data


def receive_record(args):
    """ Receives Record using a DeserializingConsumer & AvroDeserializer """
    topics = [args.topic.rstrip()]

    schema_registry_config = {
        'url': args.schema_registry }
    schema_registry_client = SchemaRegistryClient(schema_registry_config)

    avro_deserializer = AvroDeserializer(
        schema_registry_client,
        DATA_SCHEMA,
        dict_to_data)

    string_deserializer = StringDeserializer('utf_8')

    consumer_config = {
        'bootstrap.servers': args.bootstrap_servers,
        'key.deserializer': string_deserializer,
        'value.deserializer': avro_deserializer,
        'group.id': args.group,
        'auto.offset.reset': 'earliest'
    }

    consumer = DeserializingConsumer(consumer_config)
    consumer.subscribe(topics)

    print(f'Consuming data records from topic(s) {topics}. ^C to exit.')
    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(10.0)
            if msg is None:
                print('\t---Waiting. . .')
                continue

            data = msg.value()
            if data is not None:
                print(f'Data record {msg.key()}:\n'
                f'\tValues: {data}')
        except KeyboardInterrupt:
            break
    print('\nClosing consumer.')
    consumer.close()

if __name__ == "__main__":
    receive_record(receive_parse_command_line_args())
