#!/usr/bin/env python

from confluent_kafka.admin import AdminClient, NewTopic

from utils.parse_command_line_args import topic_parse_command_line_args


# Global var for creating topics & checking our main topic
PARTITIONS = 3

def check_if_topic_exists(adminclient:AdminClient, topic:str) -> bool:
    """ **DEPRECATED - Check if topic exists. Returns True or False. """

    metadata = adminclient.list_topics(timeout = 10)
    # md.topics.values is TopicMetadata
    # md.topics.keys is the topic name

    print(f'\t-Checking if topic {topic} exists. . .')
    for topic_metadata in iter(metadata.topics.values()):
        if topic_metadata.topic[0] == '_':
            continue
        if topic_metadata.error is not None:
            print(f'\t-Error with topic {topic_metadata.topic}: {topic_metadata.error}')
        else:
            print(f'\t-Found topic {topic_metadata} with '
                f'{len(topic_metadata.partitions)} partitions.')
            if len(topic_metadata.partitions) != PARTITIONS:
                print('\t-Insufficient partitions... recreating topic.')
                print(f'\t---Current Partitions: {len(topic_metadata.partitions)}')
                del_topic(adminclient, [topic_metadata.topic])
                return False
    # don't have to specify md.topics.keys, 'in' for dicts always checks keys
    return True if topic in metadata.topics else False

def print_topics_nice(topics):
    for topic in topics:
        print(f'\t--- {topic}')

def check_if_topics_exist(adminclient:AdminClient, topics:list) -> list:
    """ Check if topics exist. Returns list of topics that don't exist. """

    metadata = adminclient.list_topics(timeout = 10)
    # md.topics.values is TopicMetadata
    # md.topics.keys is the topic name

    print(f'\t-Checking if topics {topics} exist. . .')
    found = [topic for topic in topics if topic in metadata.topics]
    print('\t-Found these topics:')
    print_topics_nice(found)
    
    return list(set(topics) - set(found)) # Should return topics that weren't found

def del_topic(adminclient:AdminClient, topics:list) -> None:
    """ Delete topics """
    exists = map(check_if_topic_exists, topics)
    if False not in exists:
        print('** New Functionality from topic_setup.py: exists true')
    futures = adminclient.delete_topics(topics, operation_timeout = 30)

    for topic, future in futures.items(): # tpc is topic b/c topic is in use
        try:
            future.result()
            print(f'\t-Deleted topic {topic}')
        except Exception as e:
            print(f'\t-Error deleting topic {topic}: ',e)

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
        except Exception as e:
            print(f"\t--- Failed to create topic {topic}: {e}")

def main(args) -> None:
    """ Quality Control of our Topics """
    topics_to_be_created: list
    admin_config = {
        'bootstrap.servers': args.bootstrap_servers
    }
    adminclient = AdminClient(admin_config)
    topics = args.topic.rstrip().split(',')
    # del_topic(a, [topic])

    topics_to_be_created = check_if_topics_exist(adminclient, topics)
    if len(topics_to_be_created) > 0:
        print('\t-Topics that don\'t exist yet:')
        print_topics_nice(topics_to_be_created)

        create_topics(adminclient, topics_to_be_created)
    print('\t-Ready to go!')

    # if check_if_topic_exists(adminclient, topic):
    #     print(f'\t-Topic {topic} exists.')
    # else:
    #     print(f'\t-Topic {topic} doesn\'t exist yet!')
    #     create_topics(adminclient, [topic])

if __name__ == '__main__':
    main(topic_parse_command_line_args())
