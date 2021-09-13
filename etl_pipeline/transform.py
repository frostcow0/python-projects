import pandas as pd

def transform(data):
    data['meters_p_story'] = round(data['height_m']/data['stories'], 2) 
    return data