from argparse import ArgumentParser


def send_parse_command_line_args():
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "--topic",
        required=True,
        help="Topic name")

    arg_parser.add_argument(
        "--bootstrap-servers",
        required=False,
        default="broker:9092",
        help="Bootstrap server address")

    arg_parser.add_argument(
        "--schema-registry",
        required=False,
        default="http://schema-registry:8081",
        help="Schema Registry url")

    arg_parser.add_argument(
        "--record-key",
        required=False,
        type=str,
        help="Record key. If not provided, will be a random UUID")

    arg_parser.add_argument(
        "--record-value",
        required=True,
        type=str,
        help="Record value")

    return arg_parser.parse_args()

def receive_parse_command_line_args():
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "--topic",
        required=True,
        help="Topic name")

    arg_parser.add_argument(
        "--bootstrap-servers",
        required=False,
        default="broker:9092",
        help="Bootstrap server address")

    arg_parser.add_argument(
        "--schema-registry",
        required=False,
        default="http://schema-registry:8081",
        help="Schema Registry url")

    arg_parser.add_argument(
        "--group",
        required=False,
        default="raw_data",
        help="Consumer group")

    return arg_parser.parse_args()

def topic_parse_command_line_args():
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "--topic",
        required=True,
        help="Topic name")

    arg_parser.add_argument(
        "--bootstrap-servers",
        required=False,
        default="broker:9092",
        help="Bootstrap server address")

    arg_parser.add_argument(
        "--schema-registry",
        required=False,
        default="http://schema-registry:8081",
        help="Schema Registry url")

    return arg_parser.parse_args()