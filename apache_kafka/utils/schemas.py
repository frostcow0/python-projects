from confluent_kafka import avro, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from uuid import uuid4

data_schema = '''
{
    "namespace": "sensors",
    "type": "record",
    "name": "Data",
    "fields": [
        {
            "name": "temperature",
            "type": "int"
        },
        {
            "name": "humidity",
            "type": "int"
        },
        {
            "name": "moisture",
            "type": "int"
        },
        {
            "name": "light",
            "type": "boolean"
        }
    ]
}
'''

class Data(object):
    '''
    Data record

    Args:
        temperature (int): Temperature from sensor

        humidity (int): Humidity from sensor

        moisture (int): Moisture from sensor

        light (boolean): Light from sensor
    '''
    def __init__(self, temperature, humidity, moisture, light):
        self.temperature = temperature
        self.humidity = humidity
        self.moisture = moisture
        self.light = light

    # @staticmethod
    # def dict_to_data(obj, ctx):
    #     return Data(obj['data'])

    # @staticmethod
    # def data_to_dict(data, ctx):
    #     return Data.to_dict(data)

    # def to_dict(self):
    #     return dict(light = self.light,
    #                 moisture = self.moisture,
    #                 humidity = self.humidity,
    #                 temperature = self.temperature)

def data_to_dict(data, ctx):
    '''
    Returns a dict representation of a Data instance for serialization.

    Args:
        data (Data): Data instance.

        ctx (SerializationContext): Metadata pertaining to the serialization operation.

    Returns:
        dict: Dict populated with data attributes to be serialized.
    '''
    return dict(light = data.light,
                    moisture = data.moisture,
                    humidity = data.humidity,
                    temperature = data.temperature)
        
def dict_to_data(obj, ctx):
    '''
    Converts object literal(dict) to a Data instance.

    Args:
        obj (dict): Object literal(dict).

        ctx (SerializationContext): Metadata pertaining to the serialization operation.
    '''
    if obj is None:
        return None
    return Data(temperature = obj['temperature'],
                humidity = obj['humidity'],
                moisture = obj['moisture'],
                light = obj['light'])

environment_schema = '''
{
    "namespace": "howdyworld",
    "type": "record",
    "name": "Environment",
    "fields": [
        {
            "name": "name",
            "type": "string"
        }
    ]
}
'''

class Environment(object):
    
    __slots__ = ['name', 'id']

    def __init__(self, name=None):
        self.name = name
        self.id = uuid4()

    @staticmethod
    def dict_to_environment(obj, ctx):
        return Environment(obj['name'])

    @staticmethod
    def environment_to_dict(name, ctx):
        return Environment.to_dict(name)

    def to_dict(self):
        return dict(name=self.name)