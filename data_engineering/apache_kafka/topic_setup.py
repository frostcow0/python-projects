#!/usr/bin/env python

from confluent_kafka.admin import AdminClient, ConfigResource, NewTopic, TopicMetadata

from utils.parse_command_line_args import topic_parse_command_line_args


# Global var for creating topics & checking our main topic
PARTITIONS = 3
CONNECT_PARTITIONS = 1

def print_indent_nice(to_print:list) -> None:
    """ Decorator for printing lists of things """
    for item in to_print:
        print(f'\t\t{item}')

def del_topic(adminclient:AdminClient, topics:list) -> None:
    """ Delete topics """
    futures = adminclient.delete_topics(topics, operation_timeout = 30)
    for topic, future in futures.items():
        try:
            future.result()
            print(f'\t\tDeleted topic {topic}')
        except Exception as error:
            print(f'\t\t**Error deleting topic {topic}: ', error)

def create_topics(adminclient:AdminClient, topics:list) -> None:
    """ Create topics """
    new_topics = [NewTopic(topic,
        num_partitions=PARTITIONS,
        replication_factor=1) for topic in topics if '_connect' not in topic]
    connect_topics = [NewTopic(topic,
        num_partitions=CONNECT_PARTITIONS,
        replication_factor=1) for topic in topics if '_connect' in topic]
    if connect_topics:
        new_topics.extend(connect_topics)
    print('\tCreating topics. . .')
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
            print(f"\t\tTopic {topic} created")
        except Exception as error:
            print(f"\t\tFailed to create topic {topic}: ", error)

def get_topic_config(adminclient:AdminClient, resource:ConfigResource) -> dict:
    """ Returns resource's config as a dict """
    futures = adminclient.describe_configs(
                [resource],
                request_timeout = 20)
    topics_config = futures[resource].result()
    print(f'\t\t\tGot {resource.name}\'s config')
    return topics_config

def set_topic_config(adminclient:AdminClient, resource:ConfigResource) -> dict:
    """ Sets resource's config & returns resource's new config as a dict """
    futures = adminclient.alter_configs(
                [resource],
                request_timeout = 20)
    topics_config = futures[resource].result()
    print(f'\t\t\tSet {resource.name}\'s config')
    return topics_config

def check_topic_config(adminclient:AdminClient, topic:TopicMetadata) -> None:
    """ Checks topic's config """
    print(f'\t\tPulling config for topic {topic.topic}. . .')
    partitions = len(topic.partitions)
    if '_connect' in topic.topic: # Specific to Kafka Connect's topic needs
        correct_config = {
            'cleanup.policy': 'compact' }
        resource = ConfigResource(2, topic.topic)
        try:
            config = get_topic_config(adminclient, resource)
            new_resource = ConfigResource(2, topic.topic,
                set_config = correct_config,
                described_configs = config)
        except Exception as error:
            print('\t\t**Error getting config for topic '
            f'{topic.topic}: ', error)
        try:
            config = set_topic_config(adminclient, new_resource)
        except Exception as error:
            print('\t\t**Error setting config for topic '
            f'{topic.topic}: ', error)
        if partitions != CONNECT_PARTITIONS:
            print(f'\tInsufficient partitions ({partitions})... recreating topic {topic.topic}.')
    else:
        if partitions != PARTITIONS:
            print(f'\tInsufficient partitions ({partitions})... recreating topic {topic.topic}.')

def check_if_topics_exist(topics:list, all_topics:list) -> list:
    """ Check if topics exist. Returns list of topics that don't exist. """
    print(f'\tChecking if topics {topics} exist. . .')
    found = [topic for topic in topics if topic in all_topics]
    print('\tFound these topics:')
    print_indent_nice(found)
    return list(set(topics) - set(found)) # Returns topics that weren't found

def check_topics(adminclient:AdminClient, topics:list) -> bool:
    """ Creates topics if need be & checks the topic configs """
    metadata = adminclient.list_topics(timeout = 10)
    # md.topics.values is TopicMetadata
    # md.topics.keys is the topic name
    # ---------------------
    # Check if topics exist
    topics_to_be_created = check_if_topics_exist(
        topics,
        metadata.topics.keys())
    if topics_to_be_created: # Checks if list is empty
        create_topics(adminclient, topics_to_be_created)
        metadata = adminclient.list_topics(timeout = 10)
    # ---------------------
    # Check topics' configs
    print('\tChecking topics\' configs. . .')
    for topic in topics:
        topic_metadata = metadata.topics[topic]
        check_topic_config(adminclient, topic_metadata)
        # We get the dict of the current config, now we need to check
        # current config against what we need for connect and then
        # set the new config, and hope that the other defaults are okay :)
    return True

def main(args) -> None:
    """ Quality Control of our Topics """
    admin_config = {
        'bootstrap.servers': args.bootstrap_servers
    }
    adminclient = AdminClient(admin_config)
    topics = args.topic.rstrip().split(',')
    # del_topic(adminclient, [topic])

    if check_topics(adminclient, topics):
        print('\tReady to go!')
    else:
        print('\tSomething went wrong. . .')

if __name__ == '__main__':
    main(topic_parse_command_line_args())
