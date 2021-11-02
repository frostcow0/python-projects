#!/usr/bin/env python

from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions, ConfigResource, ConfigSource
from confluent_kafka import KafkaException
from time import sleep

from utils.parse_command_line_args import topic_parse_command_line_args


# Global var for creating topics & checking our main topic
partitions = 3

def check_if_topic_exists(a:AdminClient, topic:str) -> bool:
    '''Check if topic exists. Returns True or False.'''

    md = a.list_topics(timeout = 10)
    # md.topics.values is TopicMetadata
    # md.topics.keys is the topic name

    print(f'\t-Checking if topic {topic} exists. . .')
    for topicMetadata in iter(md.topics.values()):
        if topicMetadata.topic[0] == '_':
            continue
        if topicMetadata.error is not None:
            print(f'\t-Error with topic {topicMetadata.topic}: {topicMetadata.error}')
        else:
            print(f'\t-Found topic {topicMetadata} with {len(topicMetadata.partitions)} partitions.')
            if len(topicMetadata.partitions) != partitions:
                print(f'\t-Insufficient partitions... recreating topic.')
                del_topic(a, [topicMetadata.topic])
                return False
    
    # don't have to specify md.topics.keys, 'in' for dicts always checks keys
    return True if topic in md.topics else False

def del_topic(a:AdminClient, topics:list) -> None:
    """ Delete topics """
    exists = map(check_if_topic_exists(a), topics)
    if not False in exists:
        print('exists true')
    # while not False in exists:
    #     prin
    fs = a.delete_topics(topics, operation_timeout = 30)

    for topic, f in fs.items(): # tpc is topic b/c topic is in use
        try:
            f.result()
            print(f'\t-Deleted topic {topic}')
        except Exception as e:
            print(f'\t-Error deleting topic {topic}: ',e)

def create_topics(a:AdminClient, topics:list) -> None:
    """ Create topics """
    new_topics = [NewTopic(topic, num_partitions=partitions, replication_factor=1) for topic in topics]
    # Call create_topics to asynchronously create topics, a dict
    # of <topic,future> is returned.
    fs = a.create_topics(new_topics)

    # Wait for operation to finish.
    # Timeouts are preferably controlled by passing request_timeout=15.0
    # to the create_topics() call.
    # All futures will finish at the same time.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"\t-Topic {topic} created")
        except Exception as e:
            print(f"\t-Failed to create topic {topic}: {e}")

def main(args) -> None:
    admin_config = {
        'bootstrap.servers': args.bootstrap_servers
    }
    a = AdminClient(admin_config)
    topic = args.topic.rstrip()
    # del_topic(a, [topic])

    if check_if_topic_exists(a, topic):
        print(f'\t-Topic {topic} exists.')
    else:
        print(f'\t-Topic {topic} doesn\'t exist yet!')
        create_topics(a, [topic])

if __name__ == '__main__':
    main(topic_parse_command_line_args())