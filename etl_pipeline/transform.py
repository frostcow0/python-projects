import pandas as pd

def transform(data):
    data[6] = round(data[5]/data[3], 2)
    return data