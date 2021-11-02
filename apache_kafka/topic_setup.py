#!/usr/bin/env python

from confluent_kafka import admin
from confluent_kafka.admin import AdminClient, ConfigResource, NewTopic, TopicMetadata

from utils.parse_command_line_args import topic_parse_command_line_args


# Global var for creating topics & checking our main topic
PARTITIONS = 3

def check_topic_config(adminclient:AdminClient, topic:TopicMetadata) -> None:
    """ Checks topic's config """
    print(f'\t-Pulling config for topic {topic.topic}. . .')
    resource = ConfigResource(2, topic.topic)
    if '_connect' in topic.topic: # Specific to Kafka Connect's topic needs
        futures = adminclient.describe_configs(
            [resource],
            request_timeout = 20)
        try:
            # print(futures) # Should be None`
            print(futures[resource].result())
        except Exception as error:
            print('\t-Error getting config for topic '
            f'{topic.topic}: ',error)
    partitions = len(topic.partitions)
    if partitions != PARTITIONS:
        print(f'\t-Insufficient partitions ({partitions})... recreating topic.')

def print_indent_nice(topics:list) -> None:
    """ Decorator for printing topic names """
    for topic in topics:
        print(f'\t--- {topic}')

def check_if_topics_exist(topics:list, all_topics:list) -> list:
    """ Check if topics exist. Returns list of topics that don't exist. """
    print(f'\t-Checking if topics {topics} exist. . .')
    found = [topic for topic in topics if topic in all_topics]
    print('\t-Found these topics:')
    print_indent_nice(found)
    return list(set(topics) - set(found)) # Returns topics that weren't found

def del_topic(adminclient:AdminClient, topics:list) -> None:
    """ Delete topics """
    futures = adminclient.delete_topics(topics, operation_timeout = 30)
    for topic, future in futures.items(): # tpc is topic b/c topic is in use
        try:
            future.result()
            print(f'\t-Deleted topic {topic}')
        except Exception as error:
            print(f'\t-Error deleting topic {topic}: ',error)

def check_topics(adminclient:AdminClient, topics:list) -> bool:
    """ Creates topics if need be & checks the topic configs """
    metadata = adminclient.list_topics(timeout = 10)
    # md.topics.values is TopicMetadata
    # md.topics.keys is the topic name

    # Check if topics exist
    topics_to_be_created = check_if_topics_exist(
        topics,
        metadata.topics.keys())
    if topics_to_be_created:
        create_topics(adminclient, topics_to_be_created)

    # Check topics configs
    for topic in topics:
        topic_metadata = metadata.topics[topic]
        check_topic_config(adminclient, topic_metadata)
        # We get the dict of the current config, now we need to check
        # current config against what we need for connect and then
        # set the new config, and hope that the other defaults are okay :)

    return True



def create_topics(adminclient:AdminClient, topics:list) -> None:
    """ Create topics """
    new_topics = [NewTopic(topic,
        num_partitions=PARTITIONS,
        replication_factor=1) for topic in topics]
    print('\t-Creating topics. . .')
    # Call create_topics to asynchronously create topics, a dict
    # of <topic,future> is returned.
    futures = adminclient.create_topics(new_topics)
    # Wait for operation to finish.
    # Timeouts are preferably controlled by passing request_timeout=15.0
    # to the create_topics() call.
    # All futures will finish at the same time.
    for topic, future in futures.items():
        try:
            future.result()  # The result itself is None
            print(f"\t--- Topic {topic} created")
        except Exception as error:
            print(f"\t--- Failed to create topic {topic}: {error}")

def main(args) -> None:
    """ Quality Control of our Topics """
    admin_config = {
        'bootstrap.servers': args.bootstrap_servers
    }
    adminclient = AdminClient(admin_config)
    topics = args.topic.rstrip().split(',')
    # del_topic(a, [topic])

    if check_topics(adminclient, topics):
        print('\t-Ready to go!')
    else:
        print('\t-Something went wrong. . .')

if __name__ == '__main__':
    main(topic_parse_command_line_args())
