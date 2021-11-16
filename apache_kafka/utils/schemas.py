DATA_SCHEMA = '''
{
    "namespace": "sensors",
    "type": "record",
    "name": "Data",
    "fields": [
        {
            "name": "envId",
            "type": "int"
        },
        {
            "name": "whenCollected",
            "type": "string"
        },
        {
            "name": "timeLightOnMins",
            "type": "int"
        },
        {
            "name": "humidity",
            "type": "int"
        },
        {
            "name": "soilMoisture",
            "type": "int"
        },
        {
            "name": "temperature",
            "type": "int"
        },
        {
            "name": "waterConsumption",
            "type": "int"
        }
    ]
}
'''

class Data(object):
    """
    Data record

    Args:
        **EXPECTS A DICTIONARY WITH THESE KEY-VALUE MAPS**

        envId (int): Unique envId for required environment variables

        whenCollected (datetime): When the data was collected

        timeLightOnMins (int): Minutes the light was on since last record

        humidity (int): Humidity from sensor

        soilMoisture (int): Moisture from sensor

        temperature (int): Temperature from sensor

        waterConsumption (int): Amount of water used since last record
    """
    def __init__(self, incomingData):
        self.envId = incomingData['envId']
        self.whenCollected = incomingData['whenCollected']
        self.timeLightOnMins = incomingData['timeLightOnMins']
        self.humidity = incomingData['humidity']
        self.soilMoisture = incomingData['soilMoisture']
        self.temperature = incomingData['temperature']
        self.waterConsumption = incomingData['waterConsumption']

def data_to_dict(data:Data, ctx):
    '''
    Returns a dict representation of a Data instance for serialization.

    Args:
        data (Data): Data instance.

        ctx (SerializationContext): Metadata pertaining to the serialization operation.

    Returns:
        dict: Dict populated with data attributes to be serialized.
    '''
    return dict(envId = data.envId,
                whenCollected = data.whenCollected,
                timeLightOnMins = data.timeLightOnMins,
                humidity = data.humidity,
                soilMoisture = data.soilMoisture,
                temperature = data.temperature,
                waterConsumption = data.waterConsumption)

def dict_to_data(obj, ctx):
    '''
    Converts object literal(dict) to a Data instance.

    Args:
        obj (dict): Object literal(dict).

        ctx (SerializationContext): Metadata pertaining to the serialization operation.
    '''
    if obj is None:
        return None
    return Data(obj)
    # return Data(envId = obj['envId'],
    #             whenCollected = obj['whenCollected'],
    #             timeLightOnMins = obj['timeLightOnMins'],
    #             humidity = obj['humidity'],
    #             soilMoisture = obj['soilMoisture'],
    #             temperature = obj['temperature'],
    #             waterConsumption = obj['waterConsumption'])
