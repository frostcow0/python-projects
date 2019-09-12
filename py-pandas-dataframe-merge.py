import pandas as pd

# create zone one governance matrix

zone_one = {

    'id': ['1', '2', '3', '4', '5'],

    'control': ['up', 'down', 'left', 'right', 'jump']}

# read zone_one data into a pandas dataframe

zone_one = pd.DataFrame(zone_one, columns=['id', 'control'])

# create zone two governance matrix

zone_two = {

    'id': ['1', '2', '3', '4', '5'],

    'control': ['up', 'down', 'left', 'right', 'n/a']}

# read zone_two data into a pandas dataframe

zone_two = pd.DataFrame(zone_two, columns=['id', 'control'])

# create list object that joins both zones

frames = [zone_one, zone_two]

# create new single dataframe object that concatenates both dataframes

zone_control_map = pd.concat(frames, keys=['zone_one', 'zone_two'])

# print out the results of new dataframe

print(zone_control_map)